# src/load/load_data.py
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

# Configure logging
log_path = Path(__file__).resolve().parent.parent / 'logs' / 'data_load.log'
logging.basicConfig(
    filename = log_path,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
) 

# Get the database URL from env variables.
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL") 
if not DATABASE_URL:
    logging.error("DATABASE_URL is not set in the environment variables.")
    exit(1)

# Set up database connection
try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Failed to create database engine: {e}")
    exit(1)

def load_data():
    """Load processed JSON data into the database."""
    data_file_path = Path(__file__).parent.parent / 'data' / 'processed_data'/ 'data.json'

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
            logging.warning(f"Skipping invalid record: {record}")
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
                    created_at=datetime.utcnow()  # Sets the current timestamp for created_at
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
        logging.error(f"An unexpected error occured during the data load process: {e}")
