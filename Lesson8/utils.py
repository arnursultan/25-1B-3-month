import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_message(user_id, username, text):
    logging.info(f"User: {user_id} ({username}) sent message: {text}")