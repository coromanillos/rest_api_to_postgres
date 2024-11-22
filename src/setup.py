# src/db/setup.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from schema import Base  # Import your Base class from schema.py
from dotenv import load_dotenv
import os 

# Load enviornment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
	filename='../logs/setup.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set your PostgreSQL database URL
POSTGRES_DATABASE_URL = os.getenv("DATABASE_URL","postgresql://username:password@localhost:5432/yourdatabase")

# Create the engine to connect to PostgreSQL
try:
	engine = create_engine(DATABASE_URL)
	logging.info("Database engine created successfully.")
except SQLAlchemyError as e:
	logging.error(f"Error creating databse engine: {e}")
	raise


def create_tables():
    # Create all tables in the database.
    try:
    	Base.metadata.drop_all(engine)
    	logging.info("Tables dropped successfully")
    except SQLAlchemyError as e:
    	logging.error(f"Error dropping tables: {e}")
    	raise

if __name__ == "__main__":
    # Run the setup process
    logging.info("Starting database setup...")
    try:
    	create_tables()
    except Exception as e:
    	logging.error(f"An error occurred during setup: {e}")
    logging.info("Database setup completed.")
