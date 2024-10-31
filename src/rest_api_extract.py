 ##############################################
 # Title: Alpha Vantage Time Series Intraday Extract
 # Author: Christopher Romanillos
 # Description: Extract data from Alpha Vantage
 # 	rest API
 # Date: 10/27/24
 # Version: 1.0
 ##############################################

import requests
import json
import os
import yaml
from dotenv import load_dotenv
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='../logs/etl_errors.log',  # Log file path
    level=logging.INFO,                 # Log level (can be adjusted)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load configuration from config.yaml
with open('../config/config.yaml', 'r') as file:
	config = yaml.safe_load(file)

# Load API key from .env to a variable
load_dotenv()
api_key = os.getenv('API_KEY')

# Load API URL and Timeout from config.yaml to a variable
api_endpoint = config['api']['endpoint']
timeout_value = config['api']['timeout']

# Construct the full URL 
url = f"{api_endpoint}?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&adjusted=false&apikey={api_key}"

try:
	# Send the GET request with a timeout
	response = requests.get(url, timeout = timeout_value)

	# Raise an exception for HTTP errors
	response.raise_for_status()

	# Convert JSON from API into Python Dictionary
	data = response.json()

	# Log data processing for tracking
    logging.info("Data extraction and conversion successful.")
    # Optionally, save or process the data here

except requests.exceptions.Timeout:
    logging.error(f"Request timed out after {timeout_value} seconds.")
except requests.exceptions.ConnectionError:
    logging.error("A connection error occurred. Check network connection.")
except requests.exceptions.HTTPError as http_err:
    logging.error(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
    logging.error(f"An unexpected error occurred: {err}")