import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()


# ===== هندلرها =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 ربات فعاله!")


application.add_handler(CommandHandler("start", start))


# ===== webhook route =====
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"


@app.route("/")
def home():
    return "Bot is running!"


# ===== تنظیم webhook =====
async def set_webhook():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")


if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)
