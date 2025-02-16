# basic_features.py
import logging
import sqlite3
import io
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from database import add_user_log
from config import DEFAULT_OWNERS, BANNER_URL
from handlers import error_handler

logger = logging.getLogger(__name__)

# -------------------------------
# Admin Commands for Platforms and Stock
# -------------------------------

@error_handler
async def addplatform_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Adds a new reward platform.
    Usage: /addplatform <platform_name>
    """
    user_id = update.effective_user.id
    if user_id not in DEFAULT_OWNERS:
        await update.message.reply_text("❌ Access denied. Only admins can add platforms.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /addplatform <platform_name>")
        return
    platform_name = " ".join(context.args).strip()
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO platforms (name) VALUES (?)", (platform_name,))
        conn.commit()
        caption = f"🌟 Platform **{platform_name}** added successfully! 🌟"
        await update.message.reply_photo(photo=BANNER_URL, caption=caption, parse_mode=ParseMode.MARKDOWN)
        add_user_log(user_id, f"Added platform {platform_name}")
    except Exception as e:
        logger.error(f"Error adding platform: {e}")
        await update.message.reply_text("❌ Failed to add platform. It may already exist.")
    finally:
        conn.close()

@error_handler
async def addstock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Initiates adding stock for a platform.
    Usage: /addstock <platform_name>
    Then upload a TXT file with account entries.
    """
    user_id = update.effective_user.id
    if user_id not in DEFAULT_OWNERS:
        await update.message.reply_text("❌ Access denied. Only admins can add stock.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /addstock <platform_name>\nThen upload a TXT file with stock details.")
        return
    platform_name = context.args[0].strip()
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT platform_id FROM platforms WHERE name = ?", (platform_name,))
    result = c.fetchone()
    if not result:
        await update.message.reply_text(f"❌ Platform '{platform_name}' does not exist. Use /addplatform to add it.")
        conn.close()
        return
    platform_id = result[0]
    caption = (
        f"📥 **Stock Addition Initiated for {platform_name}!** 📥\n\n"
        "Please upload a TXT file containing stock details.\n"
        "Each account entry must be separated by a blank line.\n\n"
        "Example entry:\n"
        "```\n"
        "david.g.shaffer@icloud.com:Uptown07$$ | Plan = NBA League Pass Premium Season-Long | Amount = 0.00 USD/Yearly | SubscriptionStatus = Active | IsFreeTrial = NO | PaymentMethod = ApplePay | IsRenewal = YES | Expiry = 2025-09-20 | Remaining Days = 220 | Config by = @saiyanconfigs\n"
        "```"
    )
    await update.message.reply_photo(photo=BANNER_URL, caption=caption, parse_mode=ParseMode.MARKDOWN)
    context.user_data['awaiting_stock_file'] = platform_id
    conn.close()

@error_handler
async def receive_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes an uploaded TXT file containing stock details.
    Each account entry is separated by a blank line.
    """
    if 'awaiting_stock_file' not in context.user_data:
        return  # Not expecting a file.
    
    platform_id = context.user_data.pop('awaiting_stock_file')
    document = update.message.document
    if not document:
        await update.message.reply_text("❌ No document found. Please upload a TXT file.")
        return
    if not document.file_name.endswith('.txt'):
        await update.message.reply_text("❌ Invalid file type. Please upload a TXT file.")
        return

    file_obj = await document.get_file()
    file_bytes = await file_obj.download_as_bytearray()
    text = file_bytes.decode('utf-8', errors='ignore')
    
    # Split text by blank lines; each block is one account entry.
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    if not blocks:
        await update.message.reply_text("❌ No valid account details found. Ensure entries are separated by blank lines.")
        return
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    count = 0
    for block in blocks:
        try:
            c.execute("INSERT INTO stock (platform_id, account_details, is_claimed) VALUES (?, ?, 0)", (platform_id, block))
            count += 1
        except Exception as e:
            logger.error(f"Error inserting account block: {block} - {e}")
    conn.commit()
    conn.close()
    caption = f"✅ Successfully added **{count}** stock entries to platform ID {platform_id}."
    await update.message.reply_photo(photo=BANNER_URL, caption=caption, parse_mode=ParseMode.MARKDOWN)
    add_user_log(update.effective_user.id, f"Added {count} stock entries to platform ID {platform_id}")

# -------------------------------
# Rewards UI for Users
# -------------------------------

@error_handler
async def rewards_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the rewards menu with a list of reward platforms as inline buttons.
    """
    query = update.callback_query
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT platform_id, name FROM platforms")
    platforms = c.fetchall()
    conn.close()
    if not platforms:
        await query.answer("❌ No reward platforms available.")
        return
    keyboard = []
    for platform_id, name in platforms:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"platform_{platform_id}")])
    keyboard.append([InlineKeyboardButton(text="🏠 Back to Menu", callback_data="menu_main")])
    caption = "🎁 **Select a Reward Platform:**"
    await query.edit_message_media(
        media=InputMediaPhoto(media=BANNER_URL, caption=caption, parse_mode=ParseMode.MARKDOWN),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def show_platform_stock(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """
    Displays available stock for a selected platform along with a 'Claim' button.
    """
    query = update.callback_query
    try:
        platform_id = int(data.split("_")[1])
    except Exception:
        await query.answer("❌ Invalid platform selection.")
        return
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT name FROM platforms WHERE platform_id = ?", (platform_id,))
    result = c.fetchone()
    if not result:
        await query.answer("❌ Platform not found.")
        conn.close()
        return
    platform_name = result[0]
    c.execute("SELECT COUNT(*) FROM stock WHERE platform_id = ? AND is_claimed = 0", (platform_id,))
    stock_count = c.fetchone()[0]
    conn.close()
    message = f"🎯 **Platform:** {platform_name}\n💡 **Available Stock:** {stock_count}"
    keyboard = [
        [InlineKeyboardButton(text="⚡ Claim", callback_data=f"claim_{platform_id}")],
        [InlineKeyboardButton(text="🏠 Back", callback_data="menu_rewards")]
    ]
    await query.edit_message_media(
        media=InputMediaPhoto(media=BANNER_URL, caption=message, parse_mode=ParseMode.MARKDOWN),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def claim_stock(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """
    When a user taps 'Claim', selects one random unclaimed stock entry,
    marks it as claimed, retrieves the actual platform name, and sends its details.
    """
    query = update.callback_query
    try:
        platform_id = int(data.split("_")[1])
    except Exception:
        await query.answer("❌ Invalid claim request.")
        return
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute(
        "SELECT stock_id, account_details FROM stock WHERE platform_id = ? AND is_claimed = 0 ORDER BY RANDOM() LIMIT 1",
        (platform_id,)
    )
    result = c.fetchone()
    if not result:
        await query.edit_message_media(
            media=InputMediaPhoto(media=BANNER_URL, caption="❌ No available stock for this platform.", parse_mode=ParseMode.MARKDOWN),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Back", callback_data="menu_rewards")]])
        )
        conn.close()
        return
    stock_id, account_details = result
    c.execute("UPDATE stock SET is_claimed = 1 WHERE stock_id = ?", (stock_id,))
    conn.commit()
    c.execute("SELECT name FROM platforms WHERE platform_id = ?", (platform_id,))
    platform_row = c.fetchone()
    platform_name = platform_row[0] if platform_row else "Unknown Platform"
    conn.close()
    message = (
        "🎉✨ **PREMIUM ACCOUNT ACTIVATED!** ✨🎉\n\n"
        f"📦 **{platform_name} Elite Accounts**\n\n"
        "🔑 **Your Login Information:**\n\n"
        "```\nACCOUNT\n```\n\n"
        "📌 **How to Use:**\n"
        "📋 Copy the credentials carefully.\n"
        "🌍 Visit the platform website or open the app.\n"
        "🔐 Log in using these details.\n\n"
        "⚠️ **Important Reminders:**\n"
        "• 🛡️ Keep these details private.\n"
        "• 🔄 Change your password if possible.\n"
        "• ⏳ Account remains valid until revoked.\n\n"
        "Enjoy your premium experience! 🎥🍿\n"
        "For support, contact: @onecore @wantan1 @Shanksisback @MrLazyOp"
    )
    keyboard = [[InlineKeyboardButton(text="🏠 Back", callback_data="menu_rewards")]]
    await query.edit_message_media(
        media=InputMediaPhoto(media=BANNER_URL, caption=message, parse_mode=ParseMode.MARKDOWN),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
