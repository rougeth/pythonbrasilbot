import telebot
from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def hello_world(message):
    bot.reply_to(message, f"Hello, @{message.from_user.username}!")


@bot.message_handler(commands=["local", "endereço", "endereco"])
def address(message):
    bot.send_message(message.chat.id,(
        "As palestras da *Python Brasil 2019* acontecerão no endereço abaixo:\n"
        "*Centro de Convenções Ribeirão Preto*\n"
        "R. Bernardino de Campos, 999 - Centro, Ribeirão Preto - SP"
    ), parse_mode="Markdown")
    bot.send_location(message.chat.id, -21.1748969, -47.8098745)


bot.polling()
