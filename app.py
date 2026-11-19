# app.py
import os
import threading
import telebot
from flask import Flask

from translator import translate  # ваша функция из translator.py

# ============================================================
# НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ============================================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан в переменных окружения")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ============================================================
# TELEGRAM-БОТ
# ============================================================

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Отправь мне фразу (до 250 символов), и я переведу её "
        "на корпоративный и шизотерический языки.",
    )


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_text = (message.text or "").strip()

    if not user_text:
        bot.reply_to(message, "Пустое сообщение — нечего переводить.")
        return

    if len(user_text) > 250:
        bot.reply_to(
            message,
            f"Слишком длинный текст: {len(user_text)} символов. "
            f"Максимум — 250 (~3 предложения средней длины). Сократите и попробуйте снова.",
        )
        return

    try:
        result = translate(user_text)
        response = (
            f"*Корпоративный:*\n{result['corporate']}\n\n"
            f"*Шизотерический:*\n{result['esoteric']}"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


def run_bot():
    """Запускает бота в отдельном потоке."""
    bot.infinity_polling()


# ============================================================
# FLASK: HEALTH-CHECK ДЛЯ RENDER
# ============================================================

@app.route("/")
@app.route("/health")
def health():
    return "ok", 200


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    # Бот — в фоновом потоке
    threading.Thread(target=run_bot, daemon=True).start()

    # Flask — в основном потоке, слушает порт Render
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
  
