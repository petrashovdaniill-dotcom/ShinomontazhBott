from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8641697563:AAGX1bN8f2I-OZNodEp8KAHEi8Eo1MfJj8k"
ADMIN_ID
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔧 Записаться", callback_data="record")
        ],
        [
            InlineKeyboardButton("💰 Цены", callback_data="price")
        ],
        [
            InlineKeyboardButton("📍 Адрес", callback_data="address")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚗 Добро пожаловать в шиномонтаж!\n\n"
        "Выберите нужный раздел:",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "record":
        await query.message.reply_text(
            "🔧 Запись на шиномонтаж\n\n"
            "Напишите одним сообщением:\n\n"
            "👤 Имя:\n"
            "📞 Телефон:\n"
            "🚗 Автомобиль:\n"
            "🕒 Удобное время:"
        )

    elif query.data == "price":
        await query.message.reply_text(
            "💰 Наши цены:\n\n"
            "🚗 R13-R14 — 1000₽\n"
            "🚗 R15-R16 — 1500₽\n"
            "🚗 R17-R18 — 2000₽\n"
            "🚗 R19 и выше — уточняйте"
        )

    elif query.data == "address":
        await query.message.reply_text(
            "📍 Наш адрес:\n\n"
            "Укажите свой адрес здесь\n\n"
            "🕒 Работаем ежедневно"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
