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
import logging

def get_latest_file(directory: str, pattern: str = "*.json") -> Path:
    """
    Get the most recent file in a directory based on a pattern.

    Args:
        directory (str): The path to the directory to search.
        pattern (str): The file pattern to match (default is '*.json').

    Returns:
        Path: The most recently created or modified file that matches the pattern.

    Raises:
        FileNotFoundError: If no matching files are found.
        Exception: For other unexpected errors.
    """
    try:
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{directory} is not a valid directory.")

        # Match files based on the provided pattern
        files = list(dir_path.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No files matching pattern '{pattern}' found in {directory}.")

        # Return the most recently modified or created file
        latest_file = max(files, key=lambda f: f.stat().st_mtime)  # Use st_mtime for last modified
        logging.info(f"Latest file found: {latest_file}")
        return latest_file
    except Exception as e:
        logging.error(f"Error locating the latest file: {e}")
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
