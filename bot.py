import os
import csv
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token bot từ BotFather
ADMIN_ID = 7903231043               # Telegram ID của bạn

REPLY_FILE = "reply_targets.json"

def load_reply_targets():
    if os.path.exists(REPLY_FILE):
        with open(REPLY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reply_targets(data):
    with open(REPLY_FILE, "w") as f:
        json.dump(data, f)

def log_message(user_id, username, message):
    with open("messages_log.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_id, username, message])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Gửi tin nhắn cho mình nhé.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Không có username"
    message = update.message.text

    await update.message.reply_text("✅ Đã nhận tin nhắn của bạn!")

    admin_text = f"📩 Tin nhắn từ @{username} (ID: {user_id}):\n\n{message}"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Trả lời lại", callback_data=f"reply_to:{user_id}")]
    ])

    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, reply_markup=keyboard)

    log_message(user_id, username, message)

async def reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("reply_to:"):
        target_user_id = int(data.split(":")[1])
        admin_id = query.from_user.id

        reply_targets = load_reply_targets()
        reply_targets[str(admin_id)] = target_user_id
        save_reply_targets(reply_targets)

        await query.message.reply_text("💬 Nhập nội dung bạn muốn gửi cho người dùng này:")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.message.from_user.id
    reply_targets = load_reply_targets()

    if str(admin_id) in reply_targets:
        target_user_id = reply_targets.pop(str(admin_id))
        save_reply_targets(reply_targets)

        message = update.message.text

        try:
            await context.bot.send_message(chat_id=target_user_id, text=f"📬 Phản hồi từ admin:\n\n{message}")
            await update.message.reply_text("✅ Đã gửi phản hồi đến người dùng.")
        except Exception as e:
            await update.message.reply_text(f"❌ Không gửi được tin nhắn: {e}")
    else:
        await update.message.reply_text("⚠️ Bạn chưa chọn người dùng để trả lời.")

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("⚠️ BOT_TOKEN chưa được thiết lập. Vui lòng thiết lập biến môi trường BOT_TOKEN.")
        exit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(reply_button))
    app.add_handler(MessageHandler(filters.TEXT & filters.USER(ADMIN_ID), handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot đang chạy...")
    app.run_polling()
