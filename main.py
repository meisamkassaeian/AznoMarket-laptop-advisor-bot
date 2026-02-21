# main.py

import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config_engine import suggest_config

TOKEN = os.getenv("BOT_TOKEN")  # مطمئن شو تو Render متغیر محیطی رو داری

# حافظه کاربر (برای فاز 1)
user_answers = {}

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["دانشجویی", "مهندسی"],
        ["اداری", "خانگی"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "سلام! شغل شما چیست؟",
        reply_markup=reply_markup
    )

# هندل پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # مرحله اول: شغل
    if "job" not in user_answers:
        user_answers["job"] = text

        keyboard = [
            ["آفیس", "رندر"],
            ["AI", "گرافیک"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "با چه نرم‌افزارهایی کار می‌کنید؟",
            reply_markup=reply_markup
        )
        return

    # مرحله دوم: نرم‌افزار
    if "software" not in user_answers:
        user_answers["software"] = text

        keyboard = [
            ["اقتصادی", "آینده‌نگر"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "استراتژی خرید شما چیست؟",
            reply_markup=reply_markup
        )
        return

    # مرحله سوم: استراتژی
    if "strategy" not in user_answers:
        user_answers["strategy"] = text

        # تولید کانفیگ پیشنهادی
        config = suggest_config(user_answers)

        result = f"""
💡 کانفیگ پیشنهادی شما:

CPU: {config['cpu']}
RAM: {config['ram']}
Storage: {config['storage']}
GPU: {config['gpu']}
"""

        await update.message.reply_text(result)

        # پاک کردن جواب‌ها برای کاربر بعدی
        user_answers.clear()

# ساخت اپلیکیشن
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# اجرای ربات با drop_pending_updates=True تا مشکل conflict کمتر شود
app.run_polling(drop_pending_updates=True)
