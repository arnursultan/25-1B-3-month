import os
import sys
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    sys.exit("Error: BOT_TOKEN environment variable not set.")

admin_ids_str = os.getenv("ADMIN_IDS", "")
if not admin_ids_str:
    ADMIN_IDS = []
else:
    try:
        ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",")]
    except ValueError:
        sys.exit("Error: invalid ADMIN_IDS environment variable. "
                 "Should be a comma-separated list of integers.")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)