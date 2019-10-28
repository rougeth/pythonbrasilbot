from telebot import TeleBot, types
from decouple import config
from datetime import datetime
import re

from utils import inline_keyboard, get_events_by_date, get_event_template
from database import content, current_year, get_grade_opcoes, grade_chaves


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def hello_world(message):
    bot.reply_to(message, f"Hello, @{message.from_user.username}!")


@bot.message_handler(commands=["local", "endereço", "endereco"])
def address(message):
    keyboard = inline_keyboard([
        [("Tutoriais e Sprints", "endereço_tutoriais_sprints")],
        [("Palestras", "endereço_palestras")],
    ])

    bot.send_message(message.chat.id, "Para onde você quer ir?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data in [
    "endereço_tutoriais_sprints",
    "endereço_palestras",
])
def address_callback_query(callback):
    if callback.data == "endereço_palestras":
        message = (
            "📍 *Endereço das Palestras*:\n"
            "Centro de Convenções Ribeirão Preto\n"
            "Rua Bernardino de Campos, 999 - Centro\n"
            "Ribeirão Preto - SP"
        )
        lat = -21.1748969
        lon = -47.8098745
    else:
        message = (
            "📍 *Endereço dos Tutoriais e Sprints*:\n"
            "Centro Universitário Estácio de Sá\n"
            "Rua Abrahão Issa Halach, 980 - Ribeirânia\n"
            "Ribeirão Preto - SP"
        )
        lat = -21.2085655
        lon = -47.7868095

    bot.edit_message_text(
        message,
        callback.message.chat.id,
        callback.message.message_id,
        parse_mode="Markdown",
    )
    bot.send_location(callback.message.chat.id, lat, lon)


@bot.message_handler(commands=["grade", "programação", "programacao"])
def address(message):
    opcoes = get_grade_opcoes(content)

    if len(opcoes) == 0:
        bot.send_message(
            message.chat.id,
            f"Não há grade definida para o ano {current_year}"
        )
        return

    keyboard = inline_keyboard(opcoes)

    bot.send_message(
        message.chat.id,
        f"Você quer ver a grade de quais atividades da *Python Brasil {current_year}*?",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda callback: callback.data in grade_chaves(content))
def select_activity_date(callback):
    key = callback.data.split("_")
    activity_key = key[1]
    activity_label = content['grade'][activity_key]['label']

    activity = content['grade'][activity_key]
    dates = activity['datas']

    opcoes = []
    for date in dates:
        date_f = datetime.fromisoformat(date)
        opcoes.append([(date_f.strftime('%d/%m/%Y'), f"{callback.data}_{date}")])

    keyboard = inline_keyboard(opcoes)

    message = f"Você deseja ver a programação dos *{activity_label}* de qual dia?"

    bot.edit_message_text(
        message,
        callback.message.chat.id,
        callback.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda callback: re.search("^grade_[a-zA-Z]+_\d{4}-\d{2}-\d{2}$", callback.data))
def grade_dia(callback):
    key_splited = callback.data.split("_")
    activity_key = key_splited[1]
    data = key_splited[2]

    events = get_events_by_date(data)

    message = ""
    events = sorted(events, key=lambda event: event["start"]["dateTime"])
    for event in events:
        message += get_event_template(
            title=event["summary"],
            author=event["extendedProperties"]["private"]["author"],
            time=event["start"]["dateTime"],
        )

    bot.send_message(
        callback.message.chat.id,
        message,
        parse_mode="Markdown",
        reply_markup=None,
    )


bot.polling()
