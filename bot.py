import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Load environment variables from .env
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Single message with enhanced formatting and emojis
    message_text = (
        "🏢 **ZeroCodeStudios** 🏢\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👨‍💻 **Founder - Deyo** 👨‍💻\n\n"
        "👨‍💼 **Founder - Xynx** 👨‍💼\n\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    
    # Buttons with emojis arranged vertically
    keyboard = [
        [InlineKeyboardButton("🚀 Join Our Channel 🚀", url="https://t.me/zerocodestudios")],
        [InlineKeyboardButton("🌐 Deyo's Website 🌐", url="https://deyo.lol/")],
        [InlineKeyboardButton("🌐 Xynx's World 🌐", callback_data="no_action")],
        [InlineKeyboardButton("💫 More Info 💫", callback_data="more_info")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "😎 **Yo, Chill Brat!** 😎\n\n"
        "🚀 There's a **LOT** more to come! 🚀\n\n"
        "✨ **Stay tuned for:**\n"
        "▪️ Amazing features\n"
        "▪️ Cool updates\n"
        "▪️ Epic surprises\n\n"
        "🎯 **Available Commands:**\n"
        "▪️ /start - Show main menu\n"
        "▪️ /help - Show this message\n\n"
        "💫 **Keep exploring! The best is yet to come!** 💫"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Answer the callback query
    
    if query.data == "more_info":
        await query.message.reply_text(
            "📋 **Available Commands:**\n\n"
            "▪️ /start - Show main menu with links\n"
            "▪️ /help - Show this help message\n\n"
            "💡 Use these commands to navigate the bot!",
            parse_mode="Markdown"
        )
    elif query.data == "no_action":
        await query.message.reply_text("🌍 Xynx's world is amazing! Stay tuned for more updates!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
