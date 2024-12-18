import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from product import Product
from productPriorityQueue import ProductPriorityQueue


class AmazonScraper:
    def __init__(self, chromedriver_path, headless=True):    # default headless is true
        # Initialize the class with the path to the chromedriver and options for headless mode
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = self.setup_driver()
    
    # setup the selenium WebDriver
    def setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(self.chromedriver_path), options=chrome_options)
        return driver

    # scrape a single amazon page base on product query
    def scrape_amazon_page(self, min_price, max_price, min_rating, products):
        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot")))

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find all product items
        for product in soup.select(".s-result-item"):
            title = product.select_one(".a-text-normal")
            price = product.select_one(".a-price .a-offscreen")
            rating = product.select_one(".a-icon-alt")
            link_element = product.select_one(".a-link-normal")

            # Extract the details
            if title and price and rating and link_element:
                title = title.text.strip()
                price = price.text.strip()
                price = float(price[1:].replace(',', ''))  # Remove "$" and convert to float
                rating = rating.text.strip()
                rating = float(rating.split()[0])
                link = "https://www.amazon.com" + link_element['href'] if link_element else None

                # Apply filters (if any)
                if (min_price and price < min_price) or (max_price and price > max_price) or (min_rating and rating < min_rating):
                    continue
                
                # Create product object and insert into priority queue
                product = Product(title, price, rating, link)
                products.insert(product)

    # navigate to next page
    def navigate_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-next"))
            )
            next_button.click()
            time.sleep(3)
            return True
        except Exception as e:
            print("No more pages or error: ", e)
            return False

    # main function scrape amazon
    def scrape(self, product, min_price=None, max_price=None, min_rating=None, max_pages=5):
        current_page = 1
        url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
        self.driver.get(url)
        
        # Priority Queue for products
        products = ProductPriorityQueue()

        # Loop through multiple pages
        while current_page <= max_pages:
            print(f"Scraping page {current_page}...")
            self.scrape_amazon_page(min_price, max_price, min_rating, products)
            if not self.navigate_next_page():
                break
            current_page += 1

        # Return the cheapest product 
        return products.peek_min()

    # close web driver
    def close_driver(self):
        self.driver.quit()

