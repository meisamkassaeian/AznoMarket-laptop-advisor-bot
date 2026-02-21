# main.py

import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "سلام! 👋\n"
        "من ربات مشاور لپ‌تاپ از مجموعه‌ی ازنومارکت هستم. 💻\n"
        "چند تا سوال ازت می‌پرسم تا بهترین کانفیگ لپ‌تاپ مناسب تو رو پیدا کنم. ✅\n"
        "بیاید شروع کنیم!"
    )
    await update.message.reply_text(intro_text)

    keyboard = [
        ["دانشجویی", "مهندسی"],
        ["اداری", "خانگی"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "اول از همه، لطفاً بگو شغل یا زمینه‌ی فعالیت اصلیت چیه؟",
        reply_markup=reply_markup
    )

# هندل پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # مرحله اول: شغل
    if "job" not in user_answers:
        user_answers["job"] = text

        keyboard = [
            ["آفیس و PDF", "نرم‌افزار مهندسی / گرافیکی / رندر"],
            ["نرم‌افزار هوش مصنوعی", "کاربری خانگی ساده"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "عالی! حالا بگو با چه نوع نرم‌افزارهایی بیشتر سر و کار داری؟ "
            "این کمک می‌کنه بفهمیم لپ‌تاپی که بهت پیشنهاد می‌کنیم از نظر پردازنده و گرافیک مناسب باشه.",
            reply_markup=reply_markup
        )
        return

    # مرحله دوم: نرم‌افزار
    if "software" not in user_answers:
        user_answers["software"] = text

        keyboard = [
            ["می‌خوام اقتصادی باشه 💰", "می‌خوام آینده‌نگر باشه 🚀"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "حالا سبک خریدت چیه؟ می‌خوای با کمترین هزینه نیازت پوشش داده بشه یا می‌خوای یه لپ‌تاپ آینده‌نگر و قدرتمند داشته باشی؟",
            reply_markup=reply_markup
        )
        return

    # مرحله سوم: استراتژی خرید
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

این کانفیگ بر اساس پاسخ‌هایی که دادی، بهترین پیشنهاد ماست 🎯
"""

        # حذف کیبورد قبلی
        await update.message.reply_text(result, reply_markup=ReplyKeyboardRemove())

        # دکمه شروع دوباره
        keyboard = [["شروع دوباره 🔄"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "اگر می‌خواید دوباره تست کنید، روی دکمه زیر بزنید:",
            reply_markup=reply_markup
        )

        user_answers.clear()
        return

    # اگر کاربر روی "شروع دوباره" زد
    if text == "شروع دوباره 🔄":
        await start(update, context)
        return

# ساخت اپلیکیشن
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# اجرای ربات با drop_pending_updates=True برای جلوگیری از conflict
app.run_polling(drop_pending_updates=True)
