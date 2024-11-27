##############################################
# Title: Alpha Vantage Time Series Intraday Extract
# Author: Christopher Romanillos
# Description: Extract data from Alpha Vantage
#   rest API, timestamp, save the file
# Date: 10/27/24
# Version: 1.0
##############################################

from utils.utils import setup_logging, save_to_file, validate_data
from utils.config import load_config, load_env_variables
from utils.api_requests import fetch_api_data
from datetime import datetime
import logging

# Set up logging
setup_logging('../logs/etl_errors.log')


# Load configuration from config.yaml to a variable
config = load_config('../config/config.yaml')
api_key = load_env_variables('API_KEY')

# Build API URL
api_endpoint = config['api']['endpoint']
timeout_value = config['api']['timeout']
symbol = 'IBM'  # This can be parameterized
interval = '5min'
url = f"{api_endpoint}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&adjusted=false&apikey={api_key}"


# Create a timestamp for filenames and data tracking
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

try:
    # Fetch data from API
    data = fetch_api_data(url, timeout_value)
    
    # Validate data structure
    if not validate_data(data, expected_field='Time Series (5min)'):
        raise ValueError("Data validation failed. Expected field not found.")
    
    # Add extraction timestamp
    data['extraction_time'] = timestamp

    # Save the data
    dave_to_file(data, f"../data/raw_data/data_{timestamp}.json")

    logging.info(f"Data extracted and saved successfully")
except Exception as e:
    logging.error(f"An error occured: {e}")