##############################################
# Title: Modular File handling Script
# Author: Christopher Romanillos
# Description: modular utils script
# Date: 12/01/24
# Version: 1.0
##############################################
import os
import glob
import json
import logging
from datetime import datetime

def get_latest_raw_data_file(raw_data_dir):
    try:
        files = glob.glob(f"{raw_data_dir}/data_*.json")
        if not files:
            raise FileNotFoundError("No raw data files found.")
        return max(files, key=os.path.getctime)
    except Exception as e:
        logging.error(f"Error locating latest raw data file: {e}")
        raise

def save_processed_data(data, processed_data_dir):
    os.makedirs(processed_data_dir, exist_ok=True)
    file_name = f"{processed_data_dir}/processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, default=str)
        logging.info(f"Processed data saved to {file_name}.")
    except Exception as e:
        logging.error(f"Error saving processed data: {e}")
        raise
