from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8641697563:AAGX1bN8f2I-OZNodEp8KAHEi8Eo1MfJj8k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔧 Записаться", callback_data="record")],
        [InlineKeyboardButton("💰 Цены", callback_data="price")],
        [InlineKeyboardButton("📍 Адрес", callback_data="address")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚗 Шиномонтаж\n\nВыберите действие:",
        reply_markup=reply_markup
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
