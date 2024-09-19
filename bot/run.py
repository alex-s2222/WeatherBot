from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    )
from telegram import ReplyKeyboardMarkup

from .heandlers.main import main
from .heandlers.weather import weather


def run():
    TOKEN = ''
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", main.start))
    app.add_handler(MessageHandler(filters.LOCATION, weather.location_handler))
    app.add_handler(MessageHandler(filters.Regex('^Выбрать город$'), weather.choice_citys))
    app.add_handler(MessageHandler(filters.Regex('^⬅️ Назад в главное меню'), main.start))
    app.add_handler(MessageHandler(filters.Text(), weather.handle_message))

   

    app.run_polling()