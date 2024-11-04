##############################################
# Title: Alpha Vantage Time Series Data Validation
# Author: Christopher Romanillos
# Description: Load in raw data, process it for
# 	data validation, timestamp, save the file
# Date: 11/02/24
# Version: 1.0
##############################################

import os
import glob
import json
import logging
from datetime import datetime

# Set up logging for processing steps
logging.basicConfig(
	filename='../logs/data_processing.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

# Directory where raw data is stored
raw_data_dir = "../data/raw_data"

# Locate the latest file in the raw_data directory
def get_latest_raw_data_file():
	list_of_files = glob.glob(f"{raw_data_dir}/data_*.json")
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

# Load the latest raw data file
latest_file_path = get_latest_raw_data_file()
with open(latest_file_path, 'r') as file:
    raw_data = json.load(file)

# Extract the specific time series data
time_series_data = raw_data.get("Time Series (5min)")

# Process the data to match Prisma schema requirements
processed_data = []
for timestamp, values in time_series_data.items():
    processed_data.append({
        "timestamp": datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
        "open": float(values["1. open"]),
        "high": float(values["2. high"]),
        "low": float(values["3. low"]),
        "close": float(values["4. close"]),
        "volume": int(values["5. volume"])
    })

# Save processed data as a JSON file in a "prepared_data" folder
processed_data_dir = "../data/processed_data"
os.makedirs(processed_data_dir, exist_ok=True)

processed_filename = f"{processed_data_dir}/processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(processed_filename, 'w') as file:
    json.dump(processed_data, file, default=str)  # Ensure datetime is serialized as a string

logging.info(f"Processed data saved as {processed_filename}")
