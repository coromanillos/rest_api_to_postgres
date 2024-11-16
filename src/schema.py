# src/db/schema.py
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class IntradayData(Base):
    __tablename__ = 'intraday_data'  # Table name in PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)  # Equivalent to DateTime in Prisma
    open = Column(Float, nullable=False)  # Equivalent to Float in Prisma
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Maps to createdAt with a default of now

# After defining this schema, run `Base.metadata.create_all(engine)` to create the table.
