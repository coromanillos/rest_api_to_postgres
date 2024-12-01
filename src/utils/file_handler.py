##############################################
# Title: Modular File handling Script
# Author: Christopher Romanillos
# Description: Modular utils script
# Date: 12/01/24
# Version: 1.1
##############################################
import json
import logging
from datetime import datetime
from pathlib import Path

def get_latest_raw_data_file(raw_data_dir):
    try:
        # Using pathlib for better path handling
        raw_data_path = Path(raw_data_dir)
        # Glob pattern for matching data files
        files = list(raw_data_path.glob("data_*.json"))
        if not files:
            raise FileNotFoundError("No raw data files found.")
        
        # Return the most recently created file
        latest_file = max(files, key=lambda f: f.stat().st_ctime)
        return latest_file
    except Exception as e:
        logging.error(f"Error locating latest raw data file: {e}")
        raise

def save_processed_data(data, processed_data_dir):
    try:
        # Ensure the processed data directory exists
        processed_data_path = Path(processed_data_dir)
        processed_data_path.mkdir(parents=True, exist_ok=True)

        # Construct the file name with timestamp
        file_name = processed_data_path / f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Save the data to a JSON file
        with open(file_name, 'w') as file:
            json.dump(data, file, default=str)
        
        logging.info(f"Processed data saved to {file_name}.")
    except Exception as e:
        logging.error(f"Error saving processed data: {e}")
        raise
