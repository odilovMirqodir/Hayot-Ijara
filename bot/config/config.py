from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")
API_BASE_URL = os.getenv("API_BASE_URL")
