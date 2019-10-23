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


def filter_events_per_days(events, days):
    filtered_events = []
    for event in events:
        start = event["start"]["dateTime"]
        start = datetime.fromisoformat(start)
        if start.day in days:
            event["start"]["dateTime"] = start
            filtered_events.append(event)

    return filtered_events

def get_tutorial_events():
    events = get_calendar_events()
    return filter_events_per_days(events, [23, 24])

def get_main_events():
    events = get_calendar_events()
    return filter_events_per_days(events, [25, 26, 27])
