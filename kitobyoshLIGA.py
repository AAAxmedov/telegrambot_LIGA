import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

# 🔧 Укажи свой токен и ID группы для заявок:
BOT_TOKEN = "7968192584:AAFkHf6kErQuF_FXfjCDKpYgFxiyGzs-1bs"
GROUP_CHAT_ID = -1002700211545  # ← сюда вставь ID группы, куда отправлять заявки
ORGANIZER_ID = 256811617  # ← сюда вставь свой Telegram user ID

# 🔸 Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 🔹 Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [KeyboardButton("📤 Xabar qoldirish")],
        
    ]
    await update.message.reply_text(
        "👋 Salom sizga! \nFARG'ONA DAVLAT UNIVERSITETI\nKITOBXON YOSHLAR LIGASI\n2025-yil YOZGI MAVSUMIGA\nXUSH KELIBSIZ!!!✅",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

# 🔹 Приём сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_chat.id
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    # Сохраняем user_id
    with open("users.txt", "a+") as f:
        f.seek(0)
        ids = f.read().splitlines()
        if str(user_id) not in ids:
            f.write(f"{user_id}\n")

    # Обработка кнопок
    if text == "📤 Xabar qoldirish":
        await update.message.reply_text("✍️ Ismingiz, familiyangiz, yo'nalishingiz va guruxingiz haqida ma'lumot qoldiring")
    else:
        # Обычное сообщение — отправляем в группу
       
        full_text = f"📨 *Yangi xabar*\n{username}\nID: `{user_id}`\n\n{text}"
        try:
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=full_text, parse_mode=ParseMode.MARKDOWN)
            await update.message.reply_text("✅ Raxmat! Sizning xabaringiz jo'natildi")
        except Exception as e:
            await update.message.reply_text("❗ Xabar jo'natilmadi, Keyinroq murojaat qiling!")
            logging.error(f"Xatolik yuz berdi: {e}")

# 🔹 Рассылка
async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ORGANIZER_ID:
        await update.message.reply_text("❌ Ommaviy tarqatish huquqi yoq sizda!")
        return

    if not context.args:
        await update.message.reply_text("Ommaviy tarqatma:\n/sendall Tarqatma matni")
        return

    message_text = " ".join(context.args)

    try:
        with open("users.txt", "r") as f:
            user_ids = f.read().splitlines()

        count = 0
        for user_id in user_ids:
            try:
                await context.bot.send_message(chat_id=int(user_id), text=message_text)
                count += 1
            except:
                pass

        await update.message.reply_text(f"📬 Tarqatma {count} nafar foydalanuvchiga jo'natildi")
    except FileNotFoundError:
        await update.message.reply_text("⛔️ Tarqatma uchun foydalanuvchi yo'q")

# 🔹 ID для организатора
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Sizning ID: {update.effective_chat.id}")

# 🔹 Ошибки
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Xatolik yuz berdi:", exc_info=context.error)

# 🔹 Запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendall", send_all))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("🤖 Bot ishga tushdi!...")
    app.run_polling(drop_pending_updates=True)
