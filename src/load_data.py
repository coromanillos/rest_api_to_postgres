# src/load/load_data.py
import os
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.schema import IntradayData  # Import the IntradayData model
from datetime import datetime

# Set your PostgreSQL database URL
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdatabase"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def load_data():
    session = Session()
    
    # Load the JSON data file from the processed data directory
    data_file_path = os.path.join('data', 'processed_data', 'data.json')
    with open(data_file_path, 'r') as file:
        data = json.load(file)

    # Insert each record into the IntradayData table
    for record in data:
        new_record = IntradayData(
            timestamp=datetime.fromisoformat(record['timestamp']),
            open=record['open'],
            high=record['high'],
            low=record['low'],
            close=record['close'],
            volume=record['volume'],
            created_at=datetime.utcnow()  # Sets the current timestamp for created_at
        )
        session.add(new_record)

    # Commit all changes to the database and close the session
    session.commit()
    session.close()
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_data()
