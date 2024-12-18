<h2>Amazon AI Scraper</h2>

<h4>Overview</h4>

The Amazon AI Scraper is an intelligent tool that leverages AI and Selenium to efficiently scrape Amazon product data based on user-defined parameters. By using a language model (ChatGPT) and tools for query processing and data storage, this scraper provides a seamless way to find products matching specific criteria such as price range, ratings, and more.

<h4>Features</h4>

AI-Driven Query Interpretation: Uses ChatGPT to process user queries and extract meaningful parameters for scraping.

Dynamic Amazon Search: The scraper employs Selenium (Chrome version 104.x.x.x) to search for and extract product data.

Customizable Filters: Parameters like product name, minimum and maximum price, minimum rating, and maximum pages can be specified for precise results.

Save Results: Extracted data can be saved using the integrated "Save to Note" tool for future reference.

<h4>How It Works</h4>

Input Query:

The user provides a query such as:

"Find headphones under $50 with rating above 4, save result to note."

AI-Powered Parameter Extraction:

The query is processed through the ChatGPT-based language model to extract structured parameters, e.g.,

Product: "headphones"

Min Price: $0

Max Price: $50

Min Rating: 4.0

Amazon Scraping:
These parameters are passed into the Amazon Scraper object, which initiates a search and extracts relevant product information using Selenium.
Save & Review:
Result with lowest cost will be returned and AI decides base on user query if save to note tool should be call to save product for easy access and analysis.
