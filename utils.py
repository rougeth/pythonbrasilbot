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
