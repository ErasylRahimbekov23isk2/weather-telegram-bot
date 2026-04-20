from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

TOKEN = "8646047390:AAEm4l1AfGedjPBIIlZrcJ_OIuGSPkrhv3A"
API_KEY = "c4631be9e94547540f168ccfedca7c6c"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Я бот погоды 🌤\n\n"
        "📌 Основные команды:\n"
        "/weather город — узнать погоду\n"
        "/cityhelp — список городов и помощь\n\n"
        "💡 Пример:\n"
        "/weather Almaty"
    )


# /cityhelp
async def cityhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Поддерживаемые города:\n"
        "• Oskemen / Ust-Kamenogorsk\n"
        "• Almaty\n"
        "• Astana\n"
        "• Shymkent\n\n"
        "💡 Использование:\n"
        "/weather Almaty\n"
        "/weather Oskemen\n\n"
        "⚠️ Если город не находится — попробуй английское название"
    )


# /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("❗ Введи город: /weather Almaty")
        return

    city = " ".join(context.args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            await update.message.reply_text("❌ Город не найден. Попробуй /cityhelp")
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

    except Exception:
        await update.message.reply_text("⚠️ Ошибка сервера. Попробуй позже")


# запуск бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("cityhelp", cityhelp))

print("🤖 Бот запущен...")
app.run_polling()