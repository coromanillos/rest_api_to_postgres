# src/db/setup.py
from sqlalchemy import create_engine
from schema import Base  # Import your Base class from schema.py

# Set your PostgreSQL database URL
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdatabase"

# Create the engine to connect to PostgreSQL
engine = create_engine(DATABASE_URL)

def create_tables():
    # Create all tables in the database (this is equivalent to `CREATE TABLE` in raw SQL)
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
