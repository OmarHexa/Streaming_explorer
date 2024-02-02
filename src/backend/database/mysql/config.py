import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get environment variables
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST", "127.0.0.1")


DATABASE_URL = f"mysql+mysqlconnector://{USER_NAME}:{PASSWORD}@{HOST}:3306/streaming_explorer"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
