import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# .env fayldan o‘zgaruvchilarni yuklab olamiz
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

# Conversation bosqichlari
ASK_NAME, ASK_QUANTITY, ASK_ADDRESS, ASK_PHONE = range(4)

# Boshlash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ismingizni kiriting:")
    return ASK_NAME

# Ism qabul qilish
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Mahsulot sonini kiriting:")
    return ASK_QUANTITY

# Mahsulot soni qabul qilish
async def ask_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quantity"] = update.message.text
    await update.message.reply_text("Yetkazib berish manzilini kiriting:")
    return ASK_ADDRESS

# Manzil qabul qilish
async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("Aloqa raqamingizni kiriting:")
    return ASK_PHONE

# Raqam qabul qilish va xabar yuborish
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    # Hamma ma’lumotlarni yig‘amiz
    info = context.user_data
    message = (
        f"🛒 *Yangi buyurtma!*\n\n"
        f"👤 Ismi: {info['name']}\n"
        f"📦 Mahsulot soni: {info['quantity']}\n"
        f"📍 Manzil: {info['address']}\n"
        f"📞 Aloqa: {info['phone']}"
    )

    # Guruhga yuboramiz
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")
    await update.message.reply_text("✅ Buyurtma qabul qilindi. Tez orada siz bilan bog'lanamiz.")
    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Buyurtma bekor qilindi.")
    return ConversationHandler.END

# Botni ishga tushirish
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_quantity)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("✅ Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
