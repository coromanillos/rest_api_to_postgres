##############################################
# Title: Modular Utilities Script
# Author: Christopher Romanillos
# Description: modular utils script
# Date: 11/23/24
# Version: 1.0
##############################################
import json
import logging

def setup_logging(log_file):
    """Set up logging configuration."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def save_to_file(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file)
    logging.info(f"Data saved to {file_path}")

def validate_data(data, expected_field):
    """Validate if the expected field exists in the data."""
    if expected_field not in data:
        logging.error(f"Expected field {expected_field} not found in data.")
        return False
    return True
