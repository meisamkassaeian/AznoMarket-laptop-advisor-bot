from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from advisor import generate_config

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("دانشجویی", callback_data="user_type_دانشجویی")],
        [InlineKeyboardButton("مهندسی", callback_data="user_type_مهندسی")],
        [InlineKeyboardButton("خانگی", callback_data="user_type_خانگی")]
    ]
    await update.message.reply_text(
        "نوع کاربری را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("user_type_"):
        user_answers["user_type"] = query.data.split("_")[2]

        config = generate_config(user_answers)

        msg = "کانفیگ پیشنهادی:\n"
        for k, v in config.items():
            msg += f"{k}: {v}\n"

        await query.edit_message_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling(
    drop_pending_updates=True,
    allowed_updates=Update.ALL_TYPES
)
