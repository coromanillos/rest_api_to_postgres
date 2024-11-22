# src/load/load_data.py
import os
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.schema import IntradayData  # Import the IntradayData model
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Set your PostgreSQL database URL
load_dotenv()
DATABASE_URL = os.getenv(POSTGRES_DATABASE_URL) 
IF NOT DATABASE_URL:
    logging.error("DATABASE_URL is not set in the environment variables.")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def load_data():
    session = Session()
    data_file_path = Path('data/processed_data/data.json').resolve()

    # Load and validate JSON data
    try: 
        with open(data_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {data_file_path}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Fail to decode JSON: {e}")
        return

    # Validate JSON structure and insert records
    new_records = []
    required_keys = {'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    for record in data:
        if not required_keys.issubset(record):
            logging.warning(f"Skipping invalid record: {record}")
            continue
        new_records.append( 
            IntradayData(
                timestamp=datetime.fromisoformat(record['timestamp']),
                open=record['open'],
                high=record['high'],
                low=record['low'],
                close=record['close'],
                volume=record['volume'],
                created_at=datetime.utcnow()  # Sets the current timestamp for created_at
            )
        )
        
    # Bulk insert and handle databse errors
    try:
        session.bulk_save_objects(new_records)
        session.commit()
        logging.info(f"Successfully loaded {len(new_records)} records into the database.")
    except Exception as e:
        session.rollback()
        logging.error(f"Database operation failed: {e}")
    finally:
        session.close()
        
if __name__ == "__main__":
    load_data()
