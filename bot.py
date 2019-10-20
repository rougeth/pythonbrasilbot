import telebot


bot = telebot.TeleBot("<TELEGRAM-BOT-TOKEN>")


@bot.message_handler(commands=["start"])
def hello_world(message):
    bot.reply_to(message, f"Hello, @{message.from_user.username}!")


bot.polling()
