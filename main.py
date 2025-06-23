import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Hardcoded token (for local/testing only)
BOT_TOKEN = "8010389350:AAHAWzh8DnTkBDUD3pvxWQnEdauT8eOjwfs"
ADMIN_ID = 1289922412
PREMIUM_FILE = "premium_users.json"

def load_premium_users():
    if not os.path.exists(PREMIUM_FILE):
        return []
    with open(PREMIUM_FILE, "r") as f:
        return json.load(f)

def save_premium_users(users):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(users, f)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎬 Welcome to MovieMitraHD!\nType /movies to browse.")

def movies(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    buttons = [
        [InlineKeyboardButton("🔥 Action Movie", callback_data="action")],
        [InlineKeyboardButton("😍 Romantic Movie", callback_data="romantic")],
    ]
    if user_id in load_premium_users():
        buttons.append([InlineKeyboardButton("🔐 Premium Movie", callback_data="premium")])
    else:
        buttons.append([InlineKeyboardButton("🔐 Premium Movie (Locked)", callback_data="locked")])
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Choose a category:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    if query.data == "action":
        query.edit_message_text("🎬 Action Movie: https://example.com/action")
    elif query.data == "romantic":
        query.edit_message_text("💕 Romantic Movie: https://example.com/romantic")
    elif query.data == "premium":
        if user_id in load_premium_users():
            query.edit_message_text("🔐 Premium Movie: https://example.com/premium")
        else:
            query.edit_message_text("❌ You are not a premium user.")
    elif query.data == "locked":
        query.edit_message_text("🔒 This is only for premium users.")

def add_premium(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized.")
        return
    try:
        new_id = int(context.args[0])
        users = load_premium_users()
        if new_id not in users:
            users.append(new_id)
            save_premium_users(users)
            update.message.reply_text(f"✅ User {new_id} added as premium.")
        else:
            update.message.reply_text("ℹ️ User is already premium.")
    except (IndexError, ValueError):
        update.message.reply_text("❗ Usage: /addpremium <user_id>")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("movies", movies))
    dp.add_handler(CommandHandler("addpremium", add_premium))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()