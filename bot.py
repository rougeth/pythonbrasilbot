from telebot import TeleBot, types
from decouple import config

from utils import inline_keyboard

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
    keyboard = inline_keyboard([
        [("Tutoriais", "grade_tutoriais")],
        [("Palestras", "grade_palestras")],
        [("Sprints", "grade_sprints")],
    ])

    bot.send_message(
        message.chat.id,
        "Você quer ver a grade de quais atividades da *Python Brasil 2019*?",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda callback: callback.data in [
    "grade_tutoriais",
    "grade_palestras",
    "grade_sprints",
])
def select_activity_date(callback):
    if callback.data == "grade_tutoriais":
        message = "Você deseja ver a programação dos *tutoriais* de qual dia?"
        keyboard = inline_keyboard([
            [("23 de Outubro", "grade_tutoriais_23")],
            [("24 de Outubro", "grade_tutoriais_24")],
        ])
    elif callback.data == "grade_palestras":
        message = "Você deseja ver a programação das *palestras* de qual dia?"
        keyboard = inline_keyboard([
            [("25 de Outubro", "grade_tutoriais_25")],
            [("26 de Outubro", "grade_tutoriais_26")],
        ])

    bot.edit_message_text(
        message,
        callback.message.chat.id,
        callback.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


bot.polling()
