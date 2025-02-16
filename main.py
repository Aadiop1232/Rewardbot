# main.py
import logging
import asyncio
import nest_asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from config import TOKEN, NOTIFICATION_CHANNEL, DEFAULT_OWNERS
from database import init_db, add_admin
from handlers import (
    start,
    callback_query_handler,
    claim_key_command,
    ban_command,
    unban_command,
    add_owner_command,
    menu_help_callback
)
from basic_features import addplatform_command, addstock_command
from admin_features import givepoints_command

# Patch the event loop (useful in environments like Termux)
nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)
logger = logging.getLogger(__name__)

def add_default_owners():
    # Add default owners (admins with the "owner" role) from config.
    for owner_id in DEFAULT_OWNERS:
        add_admin(owner_id, role='owner')

def scheduled_notification(context):
    # Send a scheduled notification to the notification channel.
    import asyncio
    asyncio.create_task(
        context.bot.send_message(
            chat_id=NOTIFICATION_CHANNEL,
            text="🔔 Scheduled Notification: Please check the admin panel for updates."
        )
    )

async def main():
    # Initialize the database and add default owner admins.
    init_db()
    add_default_owners()
    
    # Build the application.
    application = ApplicationBuilder().token(TOKEN).build()

    # Register core command handlers.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("claim", claim_key_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("addowner", add_owner_command))
    application.add_handler(CommandHandler("addplatform", addplatform_command))
    application.add_handler(CommandHandler("addstock", addstock_command))
    application.add_handler(CommandHandler("givepoints", givepoints_command))
    application.add_handler(CommandHandler("help", menu_help_callback))
    
    # Register callback query handler for inline buttons.
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    
    # Fallback message handler for unrecognized text.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                            lambda update, context: update.message.reply_text("Command not recognized. Use /help for assistance.")))
    
    # Schedule periodic notifications.
    job_queue = application.job_queue
    job_queue.run_repeating(scheduled_notification, interval=3600, first=10)
    
    # Start polling.
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
    
