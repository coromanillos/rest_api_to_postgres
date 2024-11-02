##############################################
# Title: Alpha Vantage Time Series Intraday Extract
# Author: Christopher Romanillos
# Description: Extract data from Alpha Vantage
#   rest API, timestamp, save the file
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

# Load configuration from config.yaml to a variable
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

# Create a timestamp for filenames and data tracking
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

try:
    # Send the GET request with a timeout
    response = requests.get(url, timeout=timeout_value)
    response.raise_for_status()

    # Convert JSON from API into Python Dictionary
    data = response.json()

    # Validate if the data received has expected fields
    if 'Time Series (5min)' not in data:
        logging.error("Unexpected data structure in API response.")
        raise ValueError("Data validation failed. Expected field not found in response.")

    # Add timestamp to data for tracking (if saving or further processing)
    data['extraction_time'] = timestamp

    # Save the data to a timestamped file
    filename = f"../data/raw_data/data_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(data, file)

    # Log data processing for tracking
    logging.info(f"All tests passed. Saved as {filename}")

except requests.exceptions.Timeout:
    logging.error(f"Request timed out after {timeout_value} seconds.")
except requests.exceptions.ConnectionError:
    logging.error("A connection error occurred. Check network connection.")
except requests.exceptions.HTTPError as http_err:
    logging.error(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
    logging.error(f"An unexpected error occurred: {err}")
except ValueError as valid_err:
    logging.error(f"Data validation error: {valid_err}")
except Exception as save_err:
    logging.error(f"Error saving file: {save_err}")
