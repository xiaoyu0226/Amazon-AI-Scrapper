from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from amazonScraper import AmazonScraper  # Import the scrape function from amazon_scraper.py
from prompt import *
import json

load_dotenv()  # Load environment variables

# Set up OpenAI language model
llm = ChatOpenAI(temperature=0.3)  # temperature ranges from 0.0 to 1.0, low -> more predictable, high -> more creative

# Initialize memory for conversation state
memory = ConversationBufferMemory(memory_key="chat_history")

# Langchain tool that interacts with Amazon
def amazon_search_tool(query):
    prompt = PromptTemplate(input_variables=["query"], template=amazon_query_prompt)
    formatted_prompt = prompt.format(query = query)
    response = llm(formatted_prompt)
    information = ""
    for element in response.content.split('\n'):
        information += element.strip(" ")

    information = json.loads(information)
    product = information["product"]
    min_price = information["min_price"] if information["min_price"] != "empty" else None
    max_price = information["max_price"] if information["max_price"] != "empty" else None
    min_rating = information["min_rating"] if information["min_rating"] != "empty" else None
    max_page = information["max_page"]

    amazon_scraper = AmazonScraper(chromedriver_path='/Users/xiaoyu/Downloads/chromedriver', headless = False)
    rtn_product = amazon_scraper.scrape(product, min_price, max_price, min_rating, max_page)
    if rtn_product:
        return repr(rtn_product)
    else:
        return "Sorry, I cannot find a product that matches your criteria"

# Langchain tool setup for saving notes (only when explicitly requested)
def save_product_to_notes(product_info):
    # Check if product_info is a string (which needs to be parsed)
    if isinstance(product_info, str):
        product_info = "{" + product_info.split("{")[-1]
        product_info = product_info.split("}")[0] + "}"
        product_info = product_info.replace("'", "\"")
        try:
            # Try parsing the string as a JSON (dictionary)
            product = json.loads(product_info)
        except json.JSONDecodeError as e:
            return f"Error parsing product info string: {e}"

    try:
        # Open the file in append mode
        with open("product_notes.txt", "a") as file:
            file.write(f"Product Name: {product['title']}\n")
            file.write(f"Price: {product['price']}\n")
            file.write(f"Rating: {product['rating']}\n")
            file.write(f"Link: {product['link']}\n")
            file.write("\n" + "\n") 
        return "Product information has been saved to product_notes.txt."
    except Exception as e:
        return f"Error saving product to notes: {e}"

# Langchain tool setup for Amazon search
amazon_search = Tool(
    name="AmazonSearch",
    func=amazon_search_tool,
    description="Search Amazon for products based on user preferences such as price, rating and number of pages to search."
)

# Langchain tool setup for saving notes
save_note_tool = Tool(
    name="SaveProductNote",
    func=save_product_to_notes,
    description="Saves the one product information (name, price, rating, link) returned by AmazonSearch."
)

# Function to handle user input and guide the conversation
def chatbot_query(agent):
    print("Hello! I'm your shopping assistant on Amazon! What product are you looking for?")

    # Loop for continuous conversation
    while True:
        user_input = input("You: ")

        if "quit" in user_input.lower():
            print("Goodbye! Have a nice day!")
            break

        # Run the Langchain agent to process the user input
        try:
            response = agent.run(user_input)
            if isinstance(response, str):  
                print(f"Bot: {response}") 

            else:
                print("Bot: Sorry, I couldn't find any products based on your criteria.")
        
        except Exception as e:
            print(f"Bot Error: {str(e)}")

if __name__ == "__main__":

    # Initialize Langchain agent with memory and tools
    agent = initialize_agent(
        [amazon_search, save_note_tool],
        llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    # Run the chatbot
    chatbot_query(agent)
