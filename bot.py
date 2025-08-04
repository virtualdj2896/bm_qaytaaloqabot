import os
import asyncio
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

# .env orqali o'qiladi
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))  # -100 bilan boshlanadi

# Har bir foydalanuvchi uchun vaqtincha ma'lumot saqlash
user_data_dict = {}

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = {'name': update.message.from_user.full_name}
    await update.message.reply_text("Qancha mahsulot kerak?")
    return ASK_PRODUCT

# Mahsulot soni
async def ask_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['product'] = update.message.text
    await update.message.reply_text("Yetkazib berish manzilini kiriting:")
    return ASK_ADDRESS

# Manzil
async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['address'] = update.message.text
    await update.message.reply_text("Aloqa uchun telefon raqamingizni kiriting:")
    return ASK_PHONE

# Telefon va yakunlash
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]['phone'] = update.message.text

    data = user_data_dict[user_id]
    message = (
        f"📦 *Yangi buyurtma!*\n"
        f"👤 Ism: {data['name']}\n"
        f"🔢 Mahsulot: {data['product']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"📞 Aloqa: {data['phone']}"
    )

    # Guruhga yuborish
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")
    await update.message.reply_text("✅ Rahmat! Buyurtmangiz qabul qilindi.")

    # Ma'lumotni tozalash
    user_data_dict.pop(user_id, None)
    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Buyurtma jarayoni bekor qilindi.")
    user_data_dict.pop(update.message.from_user.id, None)
    return ConversationHandler.END

# Asosiy ishga tushirish funksiyasi
async def main():
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
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
