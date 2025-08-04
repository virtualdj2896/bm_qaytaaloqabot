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

# Bosqichlar
ASK_PRODUCT, ASK_ADDRESS, ASK_PHONE = range(3)

# .env orqali o'qiladigan maxfiy ma'lumotlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))  # Render'da -100... formatda kiriting

# Har bir foydalanuvchi uchun alohida ma'lumot saqlanadi
user_data_dict = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = {'name': update.message.from_user.full_name}
    await update.message.reply_text("Qancha mahsulot kerak?")
    return ASK_PRODUCT

async def ask_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['product'] = update.message.text
    await update.message.reply_text("Yetkazib berish manzilini kiriting:")
    return ASK_ADDRESS

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['address'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['phone'] = update.message.text

    data = user_data_dict[user_id]
    message = (
        f"📦 *Yangi buyurtma!*\n"
        f"👤 Ism: {data['name']}\n"
        f"🔢 Mahsulot: {data['product']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"📞 Telefon: {data['phone']}"
    )

    # Guruhga yuborish
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")

    await update.message.reply_text("✅ Rahmat! Buyurtmangiz qabul qilindi.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_product)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
