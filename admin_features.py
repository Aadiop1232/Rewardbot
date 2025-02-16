# admin_features.py
import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database import add_user_log
from config import DEFAULT_OWNERS
from handlers import error_handler

logger = logging.getLogger(__name__)

@error_handler
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Add/Remove Platform", callback_data="admin_platform")],
        [InlineKeyboardButton("Add Stock", callback_data="admin_stock")],
        [InlineKeyboardButton("Add Channel", callback_data="admin_channel")],
        [InlineKeyboardButton("Admin Management", callback_data="admin_management")],
        [InlineKeyboardButton("User Section", callback_data="admin_users")],
        [InlineKeyboardButton("Key Generator", callback_data="admin_key")],
        [InlineKeyboardButton("Admin Help", callback_data="admin_help")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="menu_main")]
    ]
    await query.edit_message_text(
        text="Admin Panel:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def admin_platform_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "Platform Management:\n\n"
        "• To add a platform, use:\n"
        "      /addplatform <platform_name>\n\n"
        "• To remove a platform, use:\n"
        "      /removeplatform <platform_name>\n\n"
        "Note: Platform names are case-insensitive."
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

@error_handler
async def admin_stock_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "Stock Management:\n\n"
        "• To add stock for a platform, use:\n"
        "      /addstock <platform_name>\n"
        "   Then upload a TXT file containing account entries. Each account entry must be separated by a blank line.\n\n"
        "• To view stock, use:\n"
        "      /viewstock <platform_name>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

@error_handler
async def admin_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "Channel Management:\n\n"
        "• To add a verification channel, use:\n"
        "      /addchannel <channel_link> <channel_id>\n\n"
        "Ensure the bot is an admin in the channel for join verification."
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

@error_handler
async def admin_management_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Admin List", callback_data="admin_list")],
        [InlineKeyboardButton("Ban/Unban Admins", callback_data="admin_ban")],
        [InlineKeyboardButton("Remove Admin", callback_data="admin_remove")],
        [InlineKeyboardButton("Add Owner", callback_data="admin_add_owner")],
        [InlineKeyboardButton("Admin Logs", callback_data="admin_logs")],
        [InlineKeyboardButton("Back", callback_data="menu_admin")]
    ]
    await query.edit_message_text(
        text="Admin Management (Owner Only):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def admin_users_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "User Section:\n\n"
        "• To view the list of users, use:\n"
        "      /userlist\n\n"
        "• To ban a user, use:\n"
        "      /ban <user_id>\n\n"
        "• To unban a user, use:\n"
        "      /unban <user_id>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

@error_handler
async def admin_key_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "Key Generator:\n\n"
        "• To generate normal keys (15 points each), use:\n"
        "      /genkey normal <quantity>\n\n"
        "• To generate premium keys (35 points each), use:\n"
        "      /genkey premium <quantity>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

@error_handler
async def admin_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "Admin Help:\n\n"
        "Below is a list of admin commands and their usage:\n\n"
        "1. /addplatform <platform_name>\n"
        "   - Adds a new reward platform.\n\n"
        "2. /removeplatform <platform_name>\n"
        "   - Removes an existing platform.\n\n"
        "3. /addstock <platform_name>\n"
        "   - Initiates stock addition. After executing, upload a TXT file with account entries. "
        "Each entry should be separated by a blank line.\n\n"
        "4. /viewstock <platform_name>\n"
        "   - Displays current unclaimed stock for the platform.\n\n"
        "5. /addchannel <channel_link> <channel_id>\n"
        "   - Adds a new verification channel.\n\n"
        "6. /userlist\n"
        "   - Shows a paginated list of users.\n\n"
        "7. /ban <user_id>\n"
        "   - Bans a user from the bot.\n\n"
        "8. /unban <user_id>\n"
        "   - Unbans a previously banned user.\n\n"
        "9. /genkey normal <quantity>\n"
        "   - Generates the specified number of normal keys.\n\n"
        "10. /genkey premium <quantity>\n"
        "    - Generates the specified number of premium keys.\n\n"
        "11. /givepoints <user_id> <quantity>\n"
        "    - (Owner only) Adds points to a user's balance.\n\n"
        "Use these commands as needed. Each command must be typed exactly with the appropriate arguments."
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_admin")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))
  
