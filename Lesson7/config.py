import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if ADMIN_IDS:
    ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS.split(",")]
