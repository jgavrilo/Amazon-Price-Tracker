# Import necessary libraries and classes
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from amazon_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime

# Define a class for generating a report
class GenerateReport:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        self.data = data
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'currency': self.currency,
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        print("Creating report for item...")
        # Write the report to a JSON file
        with open(f'{DIRECTORY}/{file_name}.json', 'w') as f:
            json.dump(report, f)
        print("...Done")

    @staticmethod
    def get_now():
        # Get the current date and time
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        if not self.data:
            print("No data to sort.")
            return None
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("A problem occurred while sorting the items")
            return None


# Define a class for interacting with the Amazon website using Selenium
class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        # Set up Chrome webdriver options
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        # Set up Chrome webdriver with options
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        # Set up price filter for Amazon search
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting Script...")
        print(f"Looking for {self.search_term} products...")
        # Get product links for the specified search term
        links = self.get_product_links()
        print(links)
        if not links:
            print("Stop")
            return
        print(f"Got {len(links)} product links")
        print("Getting info about them...")
        # Get product data for each product link
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        # Quit the Chrome webdriver instance
        self.driver.quit()
        return None

    def get_product_links(self):
        # Open the Amazon website
        self.driver.get(self.base_url)
        # Enter the search term in the search bar
        element = self.driver.find_element(By.ID, "twotabsearchtextbox")

        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        # Add in the price filter to the search
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        print(f"The URL: {self.driver.current_url}")
        time.sleep(2)
        # Get the links for each product on the page and return them
        result_list = self.driver.find_elements(By.CLASS_NAME, 's-result-list')
        links = []
        try:
            results = result_list[0].find_elements(By.XPATH,
                                               "//div/div/div/div/div/div[2]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        # For each product link, get its product data and append it to the products list
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_asins(self, links):
        # Get the ASIN for each product link
        return [self.get_asin(link) for link in links]


    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data")
        # Get the product data for a single product with the specified ASIN
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        # Get the product title, seller, and price
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        # If all the required product data is available, create a product_info dictionary and return it
        if title and seller and price:
            return {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
        return None

    def get_title(self):
        # Get the title of a product
        try:
            return self.driver.find_element(By.ID, 'productTitle').text
        except Exception as e:
            print(e)
            print(r"Can't get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        # Get the seller of a product
        try:
            return self.driver.find_element(By.ID, 'bylineInfo').text
        except Exception as e:
            print(e)
            print(r"Can't get seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element(By.ID, 'apex_offerDisplay_desktop').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver(By.ID, 'availability').text
                if 'Available' in availability:
                    price = self.driver.find_element(By.ID, 'olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    def shorten_url(self, asin):
        # Shorten the product URL using the ASIN
        return self.base_url + 'dp/' + asin
    
    @staticmethod
    def get_asin(product_link):
        # Get the ASIN for a product from its URL
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]

    def convert_price(self, price):
        # Convert the product price to a float
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + price.split(",")[1]
        except:
            Exception()
        return float(price)

if __name__ == '__main__':
    # Create an instance of AmazonAPI and run it to get product data
    am = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = am.run()
    # Use the product data to generate a report
    GenerateReport(NAME, FILTERS, BASE_URL, CURRENCY, data)
