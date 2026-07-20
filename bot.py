from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8641697563:AAGX1bN8f2I-OZNodEp8KAHEi8Eo1MfJj8k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 Шиномонтаж работает!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
