 ##############################################
 # Title: Alpha Vantage Balance Sheet Extract
 # Author: Christopher Romanillos
 # Description: Extract data from Alpha Vantage
 # 	rest API
 # Date: 10/24/24
 # Version: 1.0
 ##############################################

import requests
import json
import os
import yaml
from dotenv import load_dotenv

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
	config = yaml.safe_load(file)

# Load API key from .env to a variable
load_dotenv()
api_key = os.getenv('API_KEY')

# Load API URL and Timeout from config.yaml to a variable
api_endpoint = config['api']['endpoint']
timeout_value = config['api']['timeout']

# Construct the full URL 
url = f"{api_endpoint}?function=BALANCE_SHEET&symbol=IBM&apikey={api_key}"

try:
	# Send the GET request with a timeout
	response = requests.get(url, timeout = timeout_value)

	# Raise an exception for HTTP errors
	response.raise_for_status()

	# Convert JSON from API into Python Dictionary
	data = response.json()

	# Pretty print the data
	print(json.dumps(data, indent=4))

except requests.exceptions.Timeout:
	print(f"Request timed out after {timeout_value} seconds.")
except requests.exceptions.ConnectionError:
	print(f"A connection error occurred. Check network connection.")
except requests.exceptions.HTTPError as http_err:
	print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
	print(f"An unexpected error occurred: {err}") 