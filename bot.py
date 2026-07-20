from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8641697563:AAGX1bN8f2I-OZNodEp8KAHEi8Eo1MfJj8k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔧 Записаться", callback_data="record")],
        [InlineKeyboardButton("💰 Цены", callback_data="price")],
        [InlineKeyboardButton("📍 Адрес", callback_data="address")]
    ]

    await update.message.reply_text(
        "🚗 Шиномонтаж\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "record":
        await query.message.reply_text(
            "🔧 Для записи напишите:\n\n"
            "1. Имя\n"
            "2. Номер телефона\n"
            "3. Марка автомобиля\n"
            "4. Желаемое время"
        )

    elif query.data == "price":
        await query.message.reply_text(
            "💰 Цены:\n\n"
            "🚗 R14 — 1200₽\"
            "\n🚙 R15-R16 — 1500₽\"
            "\n🚘 R17-R18 — 2000₽"
        )

    elif query.data == "address":
        await query.message.reply_text(
            "📍 Наш адрес:\n"
            "Ваш адрес здесь"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
