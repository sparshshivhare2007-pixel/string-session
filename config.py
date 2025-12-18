from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", 26658182))
API_HASH = getenv("API_HASH", "d3cdbdb3b81014c71ec60ed03d2b4d8f")
BOT_TOKEN = getenv("BOT_TOKEN", None)
OWNER_ID = int(getenv("OWNER_ID", 8353151202))
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://pusers:nycreation@nycreation.pd4klp1.mongodb.net/?retryWrites=true&w=majority&appName=NYCREATION")
MUST_JOIN = getenv("MUST_JOIN", "destinybots")
