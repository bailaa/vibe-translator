import os
import telebot
from translator import translate  # Импортируем вашу функцию

# Токен будет браться из переменной окружения на Render
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне фразу, и я переведу её на корпоративно-ебланский и эзотерико-осознанный языки.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_text = message.text
    # Здесь можно добавить проверку длины (MAX_INPUT_CHARS)
    try:
        result = translate(user_text)
        response = (
            f"*Корпоративно-ебланский:*\n{result['corporate']}\n\n"
            f"*Эзотерико-осознанный:*\n{result['esoteric']}"
        )
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запуск бота
bot.infinity_polling()
