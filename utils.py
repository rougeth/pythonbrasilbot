from datetime import datetime

import requests
from decouple import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_keyboard(menu):
    keyboard = InlineKeyboardMarkup()
    for rows in menu:
        buttons = []
        for label, data in rows:
            buttons.append(InlineKeyboardButton(
                text=label,
                callback_data=data,
            ))

        keyboard.row(*buttons)

    return keyboard


def get_calendar_events():
    content = requests.get(config("CALENDAR_URL"))
    return content.json()["items"]


def get_tutorial_events():
    events = get_calendar_events()
    tutorials = []
    for event in events:
        start = event["start"]["dateTime"]
        start = datetime.fromisoformat(start)
        if start.day in [23, 24]:
            event["start"]["dateTime"] = start
            tutorials.append(event)

    return tutorials
