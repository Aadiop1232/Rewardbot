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

@error_handler
async def givepoints_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Adds points to a user's account. Owner-only command.
    Usage: /givepoints <user_id> <points_quantity>
    """
    sender_id = update.effective_user.id
    if sender_id not in DEFAULT_OWNERS:
        await update.message.reply_text("❌ Access denied. Only owners can give points.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /givepoints <user_id> <points_quantity>")
        return
    try:
        target_user = int(context.args[0])
        points = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ User ID and points quantity must be numbers.")
        return
    try:
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, target_user))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ Successfully added {points} points to user {target_user}.")
    except Exception as e:
        logger.error(f"Error giving points: {e}")
        await update.message.reply_text("❌ An error occurred while giving points.")

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

# -------------------------------
# Rewards UI for Users (Delegated to features module)
# -------------------------------
# The rewards UI functions are in the separate features.py file.

# -------------------------------
# Callback Query Routing and Fallback for Text Commands
# -------------------------------

@error_handler
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == "verify":
        await verify_callback(update, context)
    elif data == "menu_main":
        await menu_main_callback(update, context)
    elif data == "menu_rewards":
        from features import rewards_menu
        await rewards_menu(update, context)
    elif data == "menu_account":
        await account_info_callback(update, context)
    elif data == "menu_referral":
        await referral_system_callback(update, context)
    elif data == "get_ref_link":
        await get_referral_link_callback(update, context)
    elif data == "menu_review":
        await review_callback(update, context)
    elif data == "menu_admin":
        await menu_admin_callback(update, context)
    elif data == "menu_help":
        await admin_help_callback(update, context)
    else:
        # Delegate rewards submenus and claim actions to the features module.
        if data.startswith("platform_"):
            from features import show_platform_stock
            await show_platform_stock(update, context, data)
        elif data.startswith("claim_"):
            from features import claim_stock
            await claim_stock(update, context, data)
        else:
            await query.answer("Unknown command.")

@error_handler
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ignore messages from channels.
    if update.effective_chat and update.effective_chat.type == "channel":
        return
    user_id = update.effective_user.id
    if context.user_data.get('awaiting_review'):
        review_text = update.message.text
        add_user_log(user_id, f"Review: {review_text}")
        await update.message.reply_text("Thank you for your feedback!", reply_markup=get_main_menu_keyboard())
        context.user_data['awaiting_review'] = False
    else:
        await update.message.reply_text("Command not recognized. Use /help for assistance.")

@error_handler
async def claim_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_id = update.effective_user.id
    if not args:
        await update.message.reply_text("Usage: /claim <key>")
        return
    key_input = args[0].strip()
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT key, type, points_value, is_claimed FROM keys WHERE key = ?", (key_input,))
    key_data = c.fetchone()
    if key_data:
        if key_data[3] == 1:
            await update.message.reply_text("This key has already been claimed.")
        else:
            c.execute("UPDATE keys SET is_claimed = 1 WHERE key = ?", (key_input,))
            c.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (key_data[2], user_id))
            conn.commit()
            await update.message.reply_text(f"Key claimed! You received {key_data[2]} points.")
            add_user_log(user_id, f"Claimed key {key_input} for {key_data[2]} points")
    else:
        await update.message.reply_text("Invalid key.")
    conn.close()

@error_handler
async def menu_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(text="Main Menu", reply_markup=get_main_menu_keyboard())

@error_handler
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bans a user (admin only). Usage: /ban <user_id>"""
    if not context.args:
        await update.message.reply_text("Usage: /ban <user_id>")
        return
    try:
        target_user = int(context.args[0])
    except ValueError:
        await update.message.reply_text("User ID must be a number.")
        return
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Access denied. Only admins can ban users.")
        return
    ban_user(target_user)
    await update.message.reply_text(f"User {target_user} has been banned.")

@error_handler
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unbans a user (admin only). Usage: /unban <user_id>"""
    if not context.args:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    try:
        target_user = int(context.args[0])
    except ValueError:
        await update.message.reply_text("User ID must be a number.")
        return
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Access denied. Only admins can unban users.")
        return
    unban_user(target_user)
    await update.message.reply_text(f"User {target_user} has been unbanned.")

@error_handler
async def add_owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adds a new owner (owner only). Usage: /addowner <user_id>"""
    if not context.args:
        await update.message.reply_text("Usage: /addowner <user_id>")
        return
    try:
        new_owner = int(context.args[0])
    except ValueError:
        await update.message.reply_text("User ID must be a number.")
        return
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("Access denied. Only owners can add new owners.")
        return
    add_admin(new_owner, role='owner')
    await update.message.reply_text(f"User {new_owner} has been added as an owner.")

@error_handler
async def claim_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_id = update.effective_user.id
    if not args:
        await update.message.reply_text("Usage: /claim <key>")
        return
    key_input = args[0].strip()
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT key, type, points_value, is_claimed FROM keys WHERE key = ?", (key_input,))
    key_data = c.fetchone()
    if key_data:
        if key_data[3] == 1:
            await update.message.reply_text("This key has already been claimed.")
        else:
            c.execute("UPDATE keys SET is_claimed = 1 WHERE key = ?", (key_input,))
            c.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (key_data[2], user_id))
            conn.commit()
            await update.message.reply_text(f"Key claimed! You received {key_data[2]} points.")
            add_user_log(user_id, f"Claimed key {key_input} for {key_data[2]} points")
    else:
        await update.message.reply_text("Invalid key.")
    conn.close()
    
