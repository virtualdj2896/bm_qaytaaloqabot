from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8066401006:AAGHqAw4783hEu_IiCmVEcbEe-YmqVYSZnw"  # ← bu yerga o'zingizning bot tokeningizni yozing

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Matnli xabarlar uchun echo handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Echo bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
