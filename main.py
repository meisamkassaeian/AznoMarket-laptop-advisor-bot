import os
import asyncio
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# مراحل مکالمه
START_BTN, JOB, SOFTWARE, STRATEGY = range(4)

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# ================= START (Welcome Screen) =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [["استارت 🚀"]]

    await update.message.reply_text(
        "👋 سلام!\n\n"
        "این ربات توسط مجموعه «ازنو مارکت» طراحی شده تا به شما کمک کند "
        "لپ‌تاپ مناسب نیاز خود را انتخاب کنید 💻\n\n"
        "📢 کانال تلگرام:\n"
        "https://t.me/AZNODIGITAL\n\n"
        "🌐 سایت:\n"
        "www.aznomarket.com\n\n"
        "برای شروع روی دکمه زیر بزنید 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

    return START_BTN


# ================= START BUTTON =================
async def start_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["دانشجو عمومی", "دانشجو مهندسی"],
        ["مهندس / رندر", "کاربری خانگی"],
    ]

    await update.message.reply_text(
        "💼 شغل یا نوع استفاده شما چیست؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return JOB


# ================= JOB =================
async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["job"] = update.message.text

    keyboard = [
        ["آفیس و PDF"],
        ["نرم‌افزار مهندسی / رندر"],
        ["هوش مصنوعی"],
    ]

    await update.message.reply_text(
        "🧩 بیشتر با چه نرم‌افزارهایی کار می‌کنید؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return SOFTWARE


# ================= SOFTWARE =================
async def software(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["software"] = update.message.text

    keyboard = [
        ["کمترین هزینه"],
        ["متعادل"],
        ["آینده‌نگر"],
    ]

    await update.message.reply_text(
        "💰 استراتژی خرید شما چیست؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return STRATEGY


# ================= RESULT =================
async def strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["strategy"] = update.message.text

    job = context.user_data["job"]
    software = context.user_data["software"]
    strategy = context.user_data["strategy"]

    # ===== Hard Filter ساده =====
    cpu = "U"
    gpu = "Onboard"

    if "رندر" in software or "مهندسی" in software:
        cpu = "H"
        gpu = "Dedicated"

    if "هوش مصنوعی" in software:
        cpu = "H"
        gpu = "Dedicated"

    if strategy == "کمترین هزینه":
        ram = "8GB"
    elif strategy == "متعادل":
        ram = "16GB"
    else:
        ram = "32GB"

    text = (
        "🎯 پیشنهاد کانفیگ برای شما:\n\n"
        f"🧠 CPU: سری {cpu}\n"
        f"🎮 گرافیک: {gpu}\n"
        f"💾 RAM: {ram}\n\n"
        "اگر می‌خواهید دوباره امتحان کنید، روی «استارت 🚀» بزنید 👇"
    )

    # حذف کیبورد قبلی
    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    # نمایش دوباره دکمه استارت
    keyboard = [["استارت 🚀"]]
    await update.message.reply_text(
        "شروع دوباره:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

    return START_BTN


# ================= HANDLERS =================
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START_BTN: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_btn)],
        JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, job)],
        SOFTWARE: [MessageHandler(filters.TEXT & ~filters.COMMAND, software)],
        STRATEGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, strategy)],
    },
    fallbacks=[CommandHandler("start", start)],
)

application.add_handler(conv_handler)

# ================= INIT (Webhook) =================
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(application.initialize())
loop.run_until_complete(application.start())
loop.run_until_complete(
    application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
)

# ================= WEBHOOK =================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    loop.run_until_complete(application.process_update(update))
    return "ok"

@app.route("/")
def home():
    return "AznoMarket Laptop Advisor Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
