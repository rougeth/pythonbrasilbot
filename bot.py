from telebot import TeleBot, types
from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def hello_world(message):
    bot.reply_to(message, f"Hello, @{message.from_user.username}!")


@bot.message_handler(commands=["local", "endereço", "endereco"])
def address(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(
        text="Tutoriais e Sprints",
        callback_data="endereço_tutoriais_sprints",
    ))
    keyboard.row(types.InlineKeyboardButton(
        text="Palestras",
        callback_data="endereço_palestras"
    ))

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



bot.polling()
