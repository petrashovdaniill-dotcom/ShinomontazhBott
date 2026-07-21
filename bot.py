import sqlite3
import os

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

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

NAME, PHONE, CAR, TIME = range(4)

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        car TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_order(name, phone, car, time):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (name, phone, car, time) VALUES (?, ?, ?, ?)",
        (name, phone, car, time)
    )

    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔧 Записаться",
                callback_data="record"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Прайс",
                callback_data="price"
            ),
            InlineKeyboardButton(
                "📍 Адрес",
                callback_data="address"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Контакты",
                callback_data="contacts"
            )
        ]
    ]

    text = (
        "👋 Добро пожаловать!\n\n"
        "🚗 *Шиномонтаж «АвтоМастер»*\n\n"
        "══════════════\n"
        "🔧 Быстрая запись\n"
        "💰 Актуальные цены\n"
        "📍 Как нас найти\n"
        "📞 Связаться с нами\n"
        "══════════════\n\n"
        "⏰ Работаем ежедневно:\n"
        "09:00 — 20:00"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    print(query.data)
    
    if query.data == "record":

        await query.message.reply_text(
            "👤 Напишите ваше имя:"
        )

        return NAME

    elif query.data == "price":

        await query.message.reply_text(
            "💰 Наш прайс:\n\n"
            "🚗 R14 — 1000₽\n"
            "🚙 R15-R16 — 1500₽\n"
            "🚘 R17-R18 — 2000₽\n\n"
            "Балансировка входит в стоимость."
        )

    elif query.data == "address":

        await query.message.reply_text(
            "📍 Наш адрес:\n"
            "Укажите адрес шиномонтажа"
        )

    elif query.data == "contacts":

        await query.message.reply_text(
            "📞 Контакты:\n\n"
            "+7 (999) 123-45-67\n\n"
            "⏰ Ежедневно 09:00–20:00"
        )

    elif query.data == "menu":

        await start(update, context)

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "📞 Напишите номер телефона:"
    )

    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "🚗 Напишите марку и модель автомобиля:"
    )

    return CAR

async def get_car(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["car"] = update.message.text

    await update.message.reply_text(
        "🕒 В какое время хотите приехать?"
    )

    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["time"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    car = context.user_data["car"]
    time = context.user_data["time"]

    save_order(
        name,
        phone,
        car,
        time
    )

    message = (
        "🚗 НОВАЯ ЗАЯВКА\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🚘 Авто: {car}\n"
        f"🕒 Время: {time}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔧 Новая запись",
                callback_data="record"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 Главное меню",
                callback_data="menu"
            )
        ]
    ]

    await update.message.reply_text(
        "✅ Ваша запись создана!\n\n"
        f"🚗 Автомобиль: {car}\n"
        f"🕒 Время: {time}\n\n"
        "Спасибо за обращение!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END

init_db()

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(

    entry_points=[
        CallbackQueryHandler(
            button_handler,
            pattern="^record$"
        )
    ],

    states={

        NAME: [
            MessageHandler(
                filters.TEXT,
                get_name
            )
        ],

        PHONE: [
            MessageHandler(
                filters.TEXT,
                get_phone
            )
        ],

        CAR: [
            MessageHandler(
                filters.TEXT,
                get_car
            )
        ],

        TIME: [
            MessageHandler(
                filters.TEXT,
                get_time
            )
        ],

    },

    fallbacks=[],
    allow_reentry=True
)

app.add_handler(CommandHandler("start", start))

# Сначала запись
app.add_handler(conv_handler)

# Потом остальные кнопки меню
app.add_handler(
    CallbackQueryHandler(button_handler,pattern="^(price|address|contacts|menu)$"))

app.run_polling()
