# Amazon Price Tracker

## Overview

This Python package allows you to track Amazon product prices and generate detailed reports. It uses Selenium for web scraping and provides a simple yet powerful way to keep an eye on your favorite products.

## Prerequisites

- Python 3.x
- [Selenium](https://www.selenium.dev/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jgavrilo/Amazon-Price-Tracker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Amazon-Price-Tracker
   ```
3. Install Selenium:
   ```bash
   pip install selenium
   ```

## Configuration

Edit the `amazon_config.py` file to set your preferences:

- `NAME`: Product name to track.
- `CURRENCY`: Currency symbol (e.g., "$").
- `MIN_PRICE` and `MAX_PRICE`: Price range to filter the search results.
- 
## Usage

## Running the Script with Command-Line Parameters

You can run the script with command-line parameters to specify the product name, currency, and price range. Here's how to do it:

```bash
python3 simple_tracker.py --name "Kindle" --currency "$" --min_price "50" --max_price "200"
```

This will track Kindle products with prices ranging from $50 to $200.

### Using Default Values

If you want to run the script with the default values specified in `amazon_config.py`, you can simply execute:

```bash
python3 simple_tracker.py
```

This will use the default values for `NAME`, `CURRENCY`, `MIN_PRICE`, and `MAX_PRICE` as specified in the code or `amazon_config.py`.

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
