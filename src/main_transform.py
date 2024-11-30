##############################################
# Title: Alpha Vantage Time Series Data Validation
# Author: Christopher Romanillos
# Description: Load in raw data, process it for
#   data validation, timestamp, save the file
# Date: 11/02/24
# Version: 1.0
##############################################

from utils.utils import setup_logging, save_to_file, validate_data
from utils.config import load_config, load_env_variables
from utils.api_requests import fetch_api_data
import os
import glob
from datetime import datetime

# Set up logging for processing steps
setup_logging('../logs/data_processing.log')

# Directory where raw data is stored
raw_data_dir = "../data/raw_data"

# Locate the latest file in the raw_data directory
def get_latest_raw_data_file():
    try:
        list_of_files = glob.glob(f"{raw_data_dir}/data_*.json")
        if not list_of_files:
            raise FileNotFoundError("No raw data files found in the directory.")
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except Exception as e:
        logging.error(f"Error in locating the latest raw data file: {e}")
        raise

# Load the latest raw data file
try:
    latest_file_path = get_latest_raw_data_file()
    with open(latest_file_path, 'r') as file:
        raw_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Error loading the raw data file {latest_file_path}: {e}")
    raise

# Extract the specific time series data
time_series_data = raw_data.get("Time Series (5min)")
if not time_series_data:
    logging.error("Expected field 'Time Series (5min)' not found in raw data.")
    raise ValueError("Data validation failed: 'Time Series (5min)' not found.")

# Process the data to match schema requirements
processed_data = []
for timestamp, values in time_series_data.items():
    try:
        # Validate that required fields are present
        if not all(key in values for key in ["1. open", "2. high", "3. low", "4. close", "5. volume"]):
            logging.warning(f"Missing required fields for timestamp {timestamp}. Skipping entry.")
            continue

        # Ensure valid data types
        processed_data.append({
            "timestamp": datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })
    except (ValueError, KeyError) as e:
        logging.error(f"Error processing data for timestamp {timestamp}: {e}")
        continue

# Check if processed_data is empty
if not processed_data:
    logging.error("No valid data was processed. Check raw data for issues.")
    raise ValueError("No valid data processed.")

# Save processed data as a JSON file in a "prepared_data" folder
processed_data_dir = "../data/processed_data"
os.makedirs(processed_data_dir, exist_ok=True)

processed_filename = f"{processed_data_dir}/processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
try:
    with open(processed_filename, 'w') as file:
        json.dump(processed_data, file, default=str)  # Ensure datetime is serialized as a string
    logging.info(f"All tests passed. Processed data saved as {processed_filename}")
except Exception as e:
    logging.error(f"Error saving processed data to {processed_filename}: {e}")
    raise
