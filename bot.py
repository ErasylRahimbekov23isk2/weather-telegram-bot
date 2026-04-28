from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")


# старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌤 Погода", callback_data="weather")],
        [InlineKeyboardButton("📍 Геолокация", callback_data="geo")]
    ]

    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "weather":
        await query.message.reply_text("Введи: /weather Oskemen")

    elif query.data == "geo":
        btn = KeyboardButton("Отправить геолокацию 📍", request_location=True)
        keyboard = ReplyKeyboardMarkup([[btn]], resize_keyboard=True)

        await query.message.reply_text(
            "Нажми кнопку ниже 👇",
            reply_markup=keyboard
        )


# погода по городу
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пример: /weather Oskemen")
        return

    city = " ".join(context.args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        await update.message.reply_text("Город не найден")
        return

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    await update.message.reply_text(
        f"🌍 Город: {city}\n"
        f"🌡 Температура: {temp}°C\n"
        f"🤔 Ощущается как: {feels}°C\n"
        f"☁️ Погода: {desc}\n"
        f"💨 Ветер: {wind} м/с"
    )


# погода по геолокации
async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru"
    data = requests.get(url).json()

    if "main" not in data:
        await update.message.reply_text("Ошибка получения данных 😢")
        return

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    await update.message.reply_text(
        f"📍 Погода по геолокации:\n"
        f"🌡 Температура: {temp}°C\n"
        f"🤔 Ощущается как: {feels}°C\n"
        f"☁️ Погода: {desc}\n"
        f"💨 Ветер: {wind} м/с"
    )


# запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.LOCATION, geo))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()