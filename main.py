import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

application = Application.builder().token(TOKEN).build()

# ---------- هندلر ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "ربات راهنمای انتخاب لپ‌تاپ آماده است 💻\n"
        "برای شروع دوباره /start را بزن 🚀"
    )

application.add_handler(CommandHandler("start", start))

# ---------- Flask ----------

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


# ---------- ست کردن Webhook ----------

async def setup_webhook():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")


if __name__ == "__main__":
    asyncio.run(setup_webhook())
    flask_app.run(host="0.0.0.0", port=10000)
