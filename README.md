# Amazon Price Tracker

This is a Python package that allows you to track the prices of Amazon products and generate reports based on their prices.

## Installation

To use this package, you will need to have Python 3 and the Selenium library installed on your system. You will also need to download the correct Chrome driver for your system from https://chromedriver.chromium.org/downloads.

To install the Selenium library, run the following command:

`pip install selenium`

## Usage

### Configuration

To use this package, you will need to edit the `amazon_config.py` file to set the following parameters:

- `NAME`: The name of the product you want to track
- `CURRENCY`: The currency used on Amazon in your region
- `MIN_PRICE`: The minimum price range for the product you want to track
- `MAX_PRICE`: The maximum price range for the product you want to track

### Simple Tracker

To run the simple tracker, run the `simple_tracker.py` script. This script will use the parameters you set in `amazon_config.py` to track the price of the product you specified and generate a report based on its price.

### Amazon API

The `amazon_api.py` script provides a class for scraping product data from Amazon. To use it, simply import the `AmazonAPI` class from the script and create an instance with the following parameters:

- `search_term`: The search term for the products you want to scrape
- `filters`: A dictionary of filters for the price range of the products you want to scrape
- `base_url`: The base URL for Amazon in your region
- `currency`: The currency used on Amazon in your region

Then call the `run` method of the instance to scrape the product data. The method returns a list of dictionaries, where each dictionary contains the product data for a single product.

### Report Generator

The `generate_report.py` script provides a class for generating reports based on the product data scraped with the `AmazonAPI` class. To use it, simply import the `GenerateReport` class from the script and create an instance with the following parameters:

- `file_name`: The name of the report file
- `filters`: A dictionary of filters for the price range of the products scraped with the `AmazonAPI` class
- `base_link`: The base URL for Amazon in your region
- `currency`: The currency used on Amazon in your region
- `data`: The list of dictionaries containing the product data scraped with the `AmazonAPI` class

Then call the constructor of the instance to generate the report. The report will be saved as a JSON file to the directory specified in the `amazon_config.py` script.

## Credits

This package was created by Jeremy Gavrilov.
