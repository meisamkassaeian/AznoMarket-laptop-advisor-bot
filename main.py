import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# ساخت اپ تلگرام
application = Application.builder().token(TOKEN).build()

# ------------------ هندلرها ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "این ربات برای کمک به انتخاب لپ‌تاپ طراحی شده 💻\n"
        "چند سوال ازت می‌پرسم تا بهترین کانفیگ رو پیشنهاد بدم.\n\n"
        "برای شروع /start رو بزن 🚀"
    )

application.add_handler(CommandHandler("start", start))

# ------------------ Flask ------------------

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running!"

@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# ------------------ اجرای Webhook ------------------

if __name__ == "__main__":
    application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    flask_app.run(host="0.0.0.0", port=10000)
