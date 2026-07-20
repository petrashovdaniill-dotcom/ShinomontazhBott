from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)

TOKEN = "8641697563:AAGX1bN8f2I-OZNodEp8KAHEi8Eo1MfJj8k"
ADMIN_ID = 5069557666

NAME, PHONE, CAR, TIME = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔧 Записаться", callback_data="record")],
        [InlineKeyboardButton("💰 Цены", callback_data="price")],
        [InlineKeyboardButton("📍 Адрес", callback_data="address")]
    ]

    await update.message.reply_text(
        "🚗 Добро пожаловать в шиномонтаж!\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "record":
        await query.message.reply_text("👤 Напишите ваше имя:")
        return NAME

    elif query.data == "price":
        await query.message.reply_text(
            "💰 Цены:\n\n"
            "R14 — 1000₽\n"
            "R15-R16 — 1500₽\n"
            "R17-R18 — 2000₽"
        )

    elif query.data == "address":
        await query.message.reply_text(
            "📍 Наш адрес:\nУкажите адрес шиномонтажа"
        )

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 Напишите номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("🚗 Напишите марку и модель автомобиля:")
    return CAR

async def get_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["car"] = update.message.text
    await update.message.reply_text("🕒 В какое время удобно приехать?")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text

    message = (
        "🚗 Новая заявка!\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📞 Телефон: {context.user_data['phone']}\n"
        f"🚘 Авто: {context.user_data['car']}\n"
        f"🕒 Время: {context.user_data['time']}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message
    )

    await update.message.reply_text(
        "✅ Спасибо! Ваша заявка принята."
    )

    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler)],
    states={
        NAME: [MessageHandler(filters.TEXT, get_name)],
        PHONE: [MessageHandler(filters.TEXT, get_phone)],
        CAR: [MessageHandler(filters.TEXT, get_car)],
        TIME: [MessageHandler(filters.TEXT, get_time)],
    },
    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

app.run_polling()
