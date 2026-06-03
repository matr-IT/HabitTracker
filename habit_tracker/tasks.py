from celery import shared_task

from models import Habit

from datetime import datetime

import requests
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("HabitTrakerRybM_bot")

def send_message(text, user_chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": user_chat_id,
        "text": text,
        "parse_mode": "Markdown"  # Allows basic text formatting like *bold*
    }

    response = requests.post(url, json=payload)
    return response.json()

@shared_task()
def send_msg():
    time_now = datetime.now().time()
    habit_list = Habit.objects.filter(time=time_now)
    for habit in habit_list:
        place = habit.place
        action = habit.action
        owner_chat_id = habit.owner.chat_id
        time = habit.time
        msg = f"Приветствую! Пора развивать привычку: {action} в {place} в {time}"
        send_message(msg, owner_chat_id)


