# main.py

import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config_engine import suggest_config

TOKEN = os.getenv("BOT_TOKEN")

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("شغل شما چیست؟ (دانشجویی / مهندسی / اداری / خانگی)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "job" not in user_answers:
        user_answers["job"] = text
        await update.message.reply_text("با چه نرم‌افزارهایی کار می‌کنید؟ (آفیس / رندر / AI)")
        return

    if "software" not in user_answers:
        user_answers["software"] = text
        await update.message.reply_text("استراتژی خرید؟ (اقتصادی / آینده‌نگر)")
        return

    if "strategy" not in user_answers:
        user_answers["strategy"] = text

        config = suggest_config(user_answers)

        result = f"""
💡 کانفیگ پیشنهادی شما:

CPU: {config['cpu']}
RAM: {config['ram']}
Storage: {config['storage']}
GPU: {config['gpu']}
"""

        await update.message.reply_text(result)

        user_answers.clear()

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling(drop_pending_updates=True)
