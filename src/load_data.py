##############################################
# Title: Main data loading script
# Author: Christopher Romanillos
# Description: validates and loads cleaned
# and transformed data to data lake.
# Date: 12/08/24
# Version: 1.0
##############################################
from utils.utils import setup_logging
import os
import json
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.schema import IntradayData  
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Set your PostgreSQL database URL
load_dotenv()

# Get the database URL from env variables.
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL") 
if not DATABASE_URL:
    logging.error("DATABASE_URL is not set in the environment variables.")
    exit(1) 

# Set up logging
log_file = Path(__file__).resolve().parent.parent / 'logs' / 'data_load.log'
setup_logging(log_file) 

# Set up database connection
try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Failed to create database engine: {e}")
    exit(1)

def find_most_recent_file(data_dir: Path) -> Path:
    """Find the most recent JSON file in the processed data directory."""
    try:
        most_recent_file = max(
            (file for file in data_dir.iterdir() if file.is_file() and file.suffix == '.json' and '__' in file.stem),
            key=lambda f: datetime.strptime(f.stem.split('__')[-1], '%Y%m%d%H%M%S'),
        )
        return most_recent_file
    except ValueError:
        logging.error(f"No valid JSON files found in the directory: {data_dir}")
        return None

def load_data():
    """Load processed JSON data into the database."""
    data_dir = Path(__file__).parent.parent / 'data' / 'processed_data'

    if not data_dir.exists() or not data_dir.is_dir():
        logging.error(f"Processed data directory does not exist: {data_dir}")
        return

    most_recent_file = find_most_recent_file(data_dir)
    if not most_recent_file:
        return

    # Load and validate JSON data
    data = []
    try:
        with open(data_file_path, 'r') as file:
            data = json.load(file)
            logging.info(f"Loaded data from {data_file_path}.")
    except FileNotFoundError:
        logging.error(f"File not found: {data_file_path}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return

    # Validate JSON structure and insert records
    new_records = []
    required_keys = {'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    for record in data:
        if not required_keys.issubset(record):
            logging.warning(f"Skipping invalid record: {record}. Missing keys: {missing_keys}")
            continue
        try:
            new_records.append(
                IntradayData(
                    timestamp=datetime.fromisoformat(record['timestamp']),
                    open=float(record['open']),
                    high=float(record['high']),
                    low=float(record['low']),
                    close=float(record['close']),
                    volume=int(record['volume']),
                    created_at=datetime.utcnow() 
                )
            )
        except Exception as e:
            logging.warning(f"Failed to process record: {record}, error: {e}")
        
    # Bulk insert and handle database errors
    try:
        with Session() as session:
            session.bulk_save_objects(new_records)
            session.commit()
            logging.info(f"Successfully loaded {len(new_records)} records into the database.")
    except Exception as e:
        logging.error(f"Database operation failed: {e}")
        
if __name__ == "__main__":
    logging.info("Starting data load process...")
    try:
        load_data()
        logging.info("Data load process completed successfully.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during the data load process: {e}")
