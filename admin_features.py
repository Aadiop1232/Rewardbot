# admin_features.py
import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import DEFAULT_OWNERS, BANNER_URL
from handlers import error_handler

logger = logging.getLogger(__name__)

@error_handler
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("➕ Add/Remove Platform", callback_data="admin_platform")],
        [InlineKeyboardButton("📥 Add Stock", callback_data="admin_stock")],
        [InlineKeyboardButton("📡 Add Channel", callback_data="admin_channel")],
        [InlineKeyboardButton("🔧 Admin Management", callback_data="admin_management")],
        [InlineKeyboardButton("👥 User Section", callback_data="admin_users")],
        [InlineKeyboardButton("🔑 Key Generator", callback_data="admin_key")],
        [InlineKeyboardButton("❓ Admin Help", callback_data="admin_help")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_main")]
    ]
    caption = (
        "🌟🔥 **ADMIN PANEL** 🔥🌟\n\n"
        "Welcome, esteemed administrator!\n"
        "Use the options below to manage platforms, stock, channels, users, keys, and more.\n"
        "Select an option to begin."
    )
    await query.edit_message_media(
        media=InputMediaPhoto(media=BANNER_URL, caption=caption, parse_mode=ParseMode.MARKDOWN),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def admin_platform_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "📊 **Platform Management** 📊\n\n"
        "• To add a platform, use:\n"
        "      `/addplatform <platform_name>`\n\n"
        "• To remove a platform, use:\n"
        "      `/removeplatform <platform_name>`\n\n"
        "_Note: Platform names are not case-sensitive._"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_stock_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "📥 **Stock Management** 📥\n\n"
        "• To add stock for a platform, use:\n"
        "      `/addstock <platform_name>`\n"
        "  Then upload a TXT file containing your account entries.\n"
        "  **Important:** Each account entry must be separated by a blank line.\n\n"
        "• To view stock, use:\n"
        "      `/viewstock <platform_name>`"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "📡 **Channel Management** 📡\n\n"
        "• To add a verification channel, use:\n"
        "      `/addchannel <channel_link> <channel_id>`\n\n"
        "Ensure the bot has admin rights in the channel for proper verification."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_management_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📋 Admin List", callback_data="admin_list")],
        [InlineKeyboardButton("⛔ Ban/Unban Admins", callback_data="admin_ban")],
        [InlineKeyboardButton("🗑️ Remove Admin", callback_data="admin_remove")],
        [InlineKeyboardButton("👑 Add Owner", callback_data="admin_add_owner")],
        [InlineKeyboardButton("📝 Admin Logs", callback_data="admin_logs")],
        [InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]
    ]
    message = (
        "🔧 **Admin Management (Owner Only)** 🔧\n\n"
        "Use these options to manage admin roles and monitor activity."
    )
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_users_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "👥 **User Management** 👥\n\n"
        "• To view all users, use the command:\n"
        "      `/userlist`\n\n"
        "• To ban a user, use:\n"
        "      `/ban <user_id>`\n\n"
        "• To unban a user, use:\n"
        "      `/unban <user_id>`\n"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_key_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "🔑 **Key Generator** 🔑\n\n"
        "• To generate normal keys (15 points each), use:\n"
        "      `/genkey normal <quantity>`\n\n"
        "• To generate premium keys (35 points each), use:\n"
        "      `/genkey premium <quantity>`\n\n"
        "These keys can then be claimed by users with the `/claim <key>` command."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

@error_handler
async def admin_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = (
        "❓ **Admin Help** ❓\n\n"
        "Below is a complete list of admin commands and their usage:\n\n"
        "1. **/addplatform <platform_name>**\n"
        "   ➜ Adds a new reward platform.\n\n"
        "2. **/removeplatform <platform_name>**\n"
        "   ➜ Removes an existing platform.\n\n"
        "3. **/addstock <platform_name>**\n"
        "   ➜ Initiates stock addition. Then upload a TXT file with account entries (each entry separated by a blank line).\n\n"
        "4. **/viewstock <platform_name>**\n"
        "   ➜ Displays the current unclaimed stock for the platform.\n\n"
        "5. **/addchannel <channel_link> <channel_id>**\n"
        "   ➜ Adds a new verification channel.\n\n"
        "6. **/userlist**\n"
        "   ➜ Lists all users.\n\n"
        "7. **/ban <user_id>**\n"
        "   ➜ Bans a user from the bot.\n\n"
        "8. **/unban <user_id>**\n"
        "   ➜ Unbans a previously banned user.\n\n"
        "9. **/genkey normal <quantity>**\n"
        "   ➜ Generates normal keys (15 points each).\n\n"
        "10. **/genkey premium <quantity>**\n"
        "    ➜ Generates premium keys (35 points each).\n\n"
        "11. **/givepoints <user_id> <quantity>**\n"
        "    ➜ (Owner only) Adds points to a user's balance.\n\n"
        "12. **/removeadmin <user_id>**\n"
        "    ➜ Removes a user from the admin list.\n\n"
        "13. **/adminlist**\n"
        "    ➜ Displays a list of all current admins and their roles.\n\n"
        "14. **/adminlogs**\n"
        "    ➜ Displays recent admin action logs."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_admin")]]
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

# -------------------------------
# Additional Admin Command Functions
# -------------------------------

@error_handler
async def admin_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays a list of all current admins and their roles."""
    query = update.callback_query
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT user_id, role FROM admins")
    admins = c.fetchall()
    conn.close()
    if not admins:
        message = "No admins found."
    else:
        message = "📋 **Admin List:**\n"
        for admin in admins:
            message += f"• User ID: {admin[0]}, Role: {admin[1]}\n"
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_management")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

@error_handler
async def admin_ban_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Provides instructions for banning/unbanning an admin.
    Actual banning/unbanning should be performed via text commands (/banadmin and /unbanadmin).
    """
    query = update.callback_query
    message = (
        "⛔ **Ban/Unban Admins** ⛔\n\n"
        "To ban an admin, use:\n"
        "    /banadmin <user_id>\n\n"
        "To unban an admin, use:\n"
        "    /unbanadmin <user_id>"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_management")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

@error_handler
async def admin_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Removes a user from the admin list.
    Usage: /removeadmin <user_id>
    """
    query = update.callback_query
    message = (
        "🗑️ **Remove Admin** 🗑️\n\n"
        "To remove an admin, use:\n"
        "    /removeadmin <user_id>"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_management")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

@error_handler
async def admin_add_owner_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Grants owner privileges to a user.
    Usage: /addowner <user_id>
    """
    query = update.callback_query
    message = (
        "👑 **Add Owner** 👑\n\n"
        "To grant owner privileges, use:\n"
        "    /addowner <user_id>"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_management")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

@error_handler
async def admin_logs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays recent admin logs."""
    query = update.callback_query
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT admin_id, action, timestamp FROM admin_logs ORDER BY id DESC LIMIT 10")
    logs = c.fetchall()
    conn.close()
    if not logs:
        message = "No admin logs found."
    else:
        message = "📝 **Admin Logs:**\n"
        for log in logs:
            message += f"• Admin ID: {log[0]}, Action: {log[1]}, At: {log[2]}\n"
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_management")]]
    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
