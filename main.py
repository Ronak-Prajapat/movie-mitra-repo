import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8010389350:AAHAWzh8DnTkBDUD3pvxWQnEdauT8eOjwfs"
ADMIN_ID = 1289922412
PREMIUM_FILE = "premium_users.json"

import json
import os

def load_premium_users():
    if not os.path.exists(PREMIUM_FILE):
        return []
    with open(PREMIUM_FILE, "r") as f:
        return json.load(f)

def save_premium_users(users):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(users, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to MovieMitraHD!\nType /movies to browse.")

async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "action":
        await query.edit_message_text("🎬 Action Movie: https://example.com/action")
    elif query.data == "romantic":
        await query.edit_message_text("💕 Romantic Movie: https://example.com/romantic")
    elif query.data == "premium":
        if user_id in load_premium_users():
            await query.edit_message_text("🔐 Premium Movie: https://example.com/premium")
        else:
            await query.edit_message_text("❌ You are not a premium user.")
    elif query.data == "locked":
        await query.edit_message_text("🔒 This is only for premium users.")

async def add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return
    try:
        new_id = int(context.args[0])
        users = load_premium_users()
        if new_id not in users:
            users.append(new_id)
            save_premium_users(users)
            await update.message.reply_text(f"✅ User {new_id} added as premium.")
        else:
            await update.message.reply_text("ℹ️ User is already premium.")
    except (IndexError, ValueError):
        await update.message.reply_text("❗ Usage: /addpremium <user_id>")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("movies", movies))
    app.add_handler(CommandHandler("addpremium", add_premium))
    app.add_handler(CallbackQueryHandler(button_handler))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
