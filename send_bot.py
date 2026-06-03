import requests
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("HabitTrakerRybM_bot")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"  # Allows basic text formatting like *bold*
    }

    response = requests.post(url, json=payload)
    return response.json()


# Test the function
print(send_message("Hello from my Python script!"))