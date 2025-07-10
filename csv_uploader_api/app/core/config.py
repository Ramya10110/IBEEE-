import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
API_TOKEN = os.getenv("API_TOKEN", "supersecrettoken")
LOG_FILE = os.getenv("LOG_FILE", "app.log")
