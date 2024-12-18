# Define the prompt template (as mentioned above)
amazon_query_prompt = """
You are a helpful assistant that organizes the user's query into structured search criteria for Amazon.

Extract the following details from the user's input:
- The product they are searching for (e.g., "Bluetooth speaker")
- The price range (e.g., max price $100)
- The minimum rating (e.g., minimum rating 4.0)
- The maximum search page numbers (eg. within 5 pages)
- Any other important criteria for searching

Return a dictionary with these keys:
- product: The product name
- min_price: The minimum price as float (or 'empty' if not mentioned)
- max_price: The maximum price as float (or 'empty' if not mentioned)
- min_rating: The minimum rating as float (or 'empty' if not mentioned)
- max_page: The maximum page to search as integer (or 5 if not mentioned)

User Query: "{query}"
"""