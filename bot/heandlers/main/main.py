from telegram.ext import (
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start message from user and output keyboard"""

    keyboard = [
        [KeyboardButton(text="Выбрать город")],
        [KeyboardButton(text="Отправить свою локацию для получения погоды", request_location=True)],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
            '<<Weather Bot>> \n Откуда вы хотите получить погоду',
            reply_markup=reply_markup,
        )