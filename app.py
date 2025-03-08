import logging
import sys
import os
import threading
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# токен .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MINI_APP_URL = "https://make-ton-telegram-mini-app-1.vercel.app/"

# Создаём Flask-приложение
app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template("index.html")


# Функция запуска Flask в потоке
def run_flask():
    logger.info("Запускаем Flask-сервер...")
    app.run(host='0.0.0.0', port=5000, debug=False)


# Сообщение при /start
WELCOME_MESSAGE = (
    "👋 Добро пожаловать!\n\n"
    "Нажмите кнопку ниже, чтобы открыть Mini App прямо в Telegram!"
)


async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🚀 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)


# Запуск Telegram-бота
def run_telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Запускаем Telegram-бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()

    # Запускаем Telegram-бота
    run_telegram_bot()
