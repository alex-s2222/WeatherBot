from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
import aiohttp

apikey = '38fec43af62b54a4cd787bc6ed68d941'

async def fetch_weather(session, url):

    try:
        async with session.get(url) as response:
            # логирование можно использовать loguru
            print(f"Ответ от {url}: {response.status}")
            if response.status == 200:
                data = await response.json()
                return {
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity']
                }
            else:
                return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

async def fetch_first_successful(url):
    # создаем время ожидания от сервера
    timeout = aiohttp.ClientTimeout(10)
    
    # создаем контекстный менеджер для
    async with aiohttp.ClientSession(timeout=timeout) as session:
        result = await fetch_weather(session, url)
        

        if result is not None:
            print("Получен успешный результат")
            weather_description = result.get('description', 'Нет данных')
            temperature = result.get('temperature', 'Нет данных')
            return f"Погода: {weather_description}, Температура: {temperature}°C"
        return None


async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #получаем локацию от пользователя
    user_location = update.message.location
    # делалось на скорую руку лучше брать основу и добавдять пораметры к запросу
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={user_location.latitude}&lon={user_location.longitude}&appid={apikey}&lang=ru&units=metric"
    
    #что бы пользователь понял что он отправил запрос отправляем сообщение
    message = await update.message.reply_text("Обрабатываю запрос...")
    #отправляем запрос на сервер 
    result = await fetch_first_successful(url)

    # при получении результата изменяем сообщение ожидания информации
    if result:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=f"{result}"
        )
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text="Не удалось получить данные о погоде."
        )



async def choice_citys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Сочи"), KeyboardButton("Кисловодск")],
        [KeyboardButton("Санкт-Петербург"), KeyboardButton("Казань")],
        [KeyboardButton("Ростов"), KeyboardButton('⬅️ Назад в главное меню')]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text('Выберите кнопку:', reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = update.message.text
    # делалось на скорую руку лучше брать основу и добавдять пораметры к запросу
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang=ru&units=metric"

    #что бы пользователь понял что он отправил запрос отправляем сообщение
    message = await update.message.reply_text("Обрабатываю запрос...")
    #отправляем запрос на сервер 
    result = await fetch_first_successful(url)

    # при получении результата изменяем сообщение ожидания информации
    if result:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=f"{result}"
        )

    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text="Не удалось получить данные о погоде."
        )
