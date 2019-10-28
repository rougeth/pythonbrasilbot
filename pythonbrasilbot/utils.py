from datetime import datetime

import requests
from decouple import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from pythonbrasilbot.database import content


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


def get_calendar_events(calendar_url):
    if calendar_url is None or calendar_url is '':
        raise AttributeError

    content = requests.get(calendar_url)
    return content.json()["items"]


def filter_events_per_date(events, event_date):
    event_date = datetime.fromisoformat(event_date)

    filtered_events = []
    for event in events:
        start = event["start"]["dateTime"]
        start = datetime.fromisoformat(start)
        if start.strftime('%Y-%m-%d') == event_date.strftime('%Y-%m-%d'):
            event["start"]["dateTime"] = start
            filtered_events.append(event)

    return filtered_events


def get_events_by_date(date):
    events = get_calendar_events(content['calendar_url'])
    return filter_events_per_date(events, date)


def get_event_template(title, author, time):
    message = ""
    if title is not None and title != "":
        message += f"*{title}*\n"

    if author is not None and author != "":
        message += f"- {author}\n"

    if time is not None and time != "":
        message += "- {}\n".format(time.strftime("%Hh%M"))

    message += "\n"

    return message