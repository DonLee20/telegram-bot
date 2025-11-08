import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Initialize application as None - will be created when needed
application = None

def get_application():
    """Get or create the Telegram application."""
    global application
    if application is None:
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment")
            raise ValueError("BOT_TOKEN is required")
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
    return application

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hello {user.mention_html()}! I'm your Telegram bot running on Netlify Serverless! 🚀\n\n"
        "Available commands:\n"
        "/start - Show this welcome message\n"
        "/help - Get help information\n"
        "/ping - Check if bot is alive"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "I'm a Telegram bot hosted on Netlify Serverless!\n\n"
        "Commands available:\n"
        "/start - Welcome message\n"
        "/help - This help message\n"
        "/ping - Check bot status"
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if bot is alive."""
    await update.message.reply_text("🏓 Pong! Bot is alive and running on Netlify Serverless!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

# Handler registration moved to get_application() function

async def handler(event, context):
    """Netlify serverless function handler."""
    try:
        # Parse the incoming update
        if event.get('body'):
            update_data = json.loads(event['body'])
            
            # Get or create application
            app = get_application()
            update = Update.de_json(update_data, app.bot)
            
            # Process the update
            await app.process_update(update)
            
            return {
                'statusCode': 200,
                'body': json.dumps('OK')
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No body provided')
            }
    except Exception as e:
        logger.error(f"Error processing update: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

# For Netlify serverless functions
if __name__ == "__main__":
    # This is used for local testing
    test_event = {
        'body': json.dumps({
            'update_id': 123456789,
            'message': {
                'message_id': 1,
                'from': {'id': 123, 'is_bot': False, 'first_name': 'Test'},
                'chat': {'id': 123, 'type': 'private'},
                'text': '/start',
                'date': 1234567890
            }
        })
    }
    
    import asyncio
    result = asyncio.run(handler(test_event, {}))
    print(result)