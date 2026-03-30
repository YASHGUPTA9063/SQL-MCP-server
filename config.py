import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# SQLite local database path
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "local.db")
