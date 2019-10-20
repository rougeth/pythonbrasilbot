import telebot
from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def hello_world(message):
    bot.reply_to(message, f"Hello, @{message.from_user.username}!")


bot.polling()
