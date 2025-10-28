# database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session # Import for type hinting

# 1. Load environment variables from .env file
load_dotenv()

# 2. Retrieve variables from the environment
# We use os.getenv() for safe retrieval
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 3. Construct the full database URL
# The format is: driver://user:password@host:port/dbname
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Create the SQLAlchemy Engine
# echo=True prints all SQL statements to the console (useful for debugging)
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# 5. Create the SessionLocal class
# This is a factory that will create a new database session
SessionLocal = sessionmaker(
    autocommit=False, # Don't commit automatically
    autoflush=False,  # Don't flush automatically
    bind=engine       # Bind to the engine we created
)

# 6. Create the Declarative Base class
# All database models (tables) will inherit from this
Base = declarative_base()


# 7. Dependency Injection function for FastAPI
# This function is used by FastAPI's Depends() to manage the session lifecycle
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()