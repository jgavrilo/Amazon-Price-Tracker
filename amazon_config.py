# Import the webdriver module from the Selenium library
from selenium import webdriver

# Specify the directory where the program will save the generated reports
DIRECTORY = 'reports'

# Set the name of the product to search for, the currency symbol used in the search,
# and the minimum and maximum price range to search within, respectively
NAME = "Kindle"
CURRENCY = "$"
MIN_PRICE = "0"
MAX_PRICE = "500"

# Create a dictionary to set the price range filter for the Amazon search
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}

# Set the URL for the Amazon website
BASE_URL = "http://www.amazon.com/"

# Define a function to return a webdriver instance with Chrome browser options passed as an argument
def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)

# Define a function to return an instance of webdriver.ChromeOptions()
def get_web_driver_options():
    return webdriver.ChromeOptions()

# Define a function to set the --ignore-certificate-errors flag to ignore any SSL certificate errors
def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

# Define a function to set the --incognito flag to launch the browser in incognito mode
def set_browser_as_incognito(options):
    options.add_argument('--incognito')

# Define a function to set the --headless flag to launch the browser in headless mode,
# which means that it will run in the background without displaying a browser window
def set_automation_as_head_less(options):
    options.add_argument('--headless')
