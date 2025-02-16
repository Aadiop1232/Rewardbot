# handlers.py
import logging
import sqlite3
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    InputMediaPhoto,
    ParseMode
)
from telegram.ext import CallbackContext
from config import REQUIRED_CHANNELS
from database import add_user, mark_user_verified, add_user_log, is_admin, is_owner, get_user

logger = logging.getLogger(__name__)

def get_verification_keyboard():
    """
    Builds a keyboard showing required channels (2 per row) and a 'Verify' button.
    """
    keyboard = []
    row = []
    for channel in REQUIRED_CHANNELS:
        btn = InlineKeyboardButton(text=channel, url=f"https://t.me/{channel.strip('@')}")
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="Verify", callback_data="verify")])
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    """
    Builds the main menu inline keyboard with buttons for Rewards, Account Info,
    Referral System, Review/Suggestion, and Admin Panel.
    """
    keyboard = [
        [
            InlineKeyboardButton(text="Rewards", callback_data="menu_rewards"),
            InlineKeyboardButton(text="Account Info", callback_data="menu_account"),
            InlineKeyboardButton(text="Referral System", callback_data="menu_referral")
        ],
        [
            InlineKeyboardButton(text="Review/Suggestion", callback_data="menu_review"),
            InlineKeyboardButton(text="Admin Panel", callback_data="menu_admin")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def error_handler(func):
    """
    A decorator to log any errors in the handler functions.
    """
    async def wrapper(update: Update, context: CallbackContext):
        try:
            return await func(update, context)
        except Exception as e:
            logger.error(f"Error in handler {func.__name__}: {e}")
    return wrapper

from telegram.ext import ContextTypes

@error_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command. Adds the user to the database and sends a welcome image
    with the verification keyboard if they are not an admin; admins are auto-verified.
    """
    user = update.effective_user
    add_user(user.id, user.username)
    if is_admin(user.id):
        mark_user_verified(user.id)
        await update.message.reply_text(
            "Welcome Admin/Owner! You are auto verified.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        welcome_text = (
            f"Hey {user.first_name}, Welcome To Shadow Rewards Bot!\n"
            "Please verify yourself by joining the below channels."
        )
        await update.message.reply_photo(
            photo="https://i.imgur.com/mDAjGNm.jpeg",
            caption=welcome_text,
            reply_markup=get_verification_keyboard()
        )

@error_handler
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Verifies that a user has joined all required channels. If so, marks them as verified
    and displays the main menu; otherwise, prompts the user again.
    """
    query = update.callback_query
    user_id = query.from_user.id
    not_joined = []
    for channel in REQUIRED_CHANNELS:
        try:
            member_status = (await context.bot.get_chat_member(chat_id=channel, user_id=user_id)).status
            if member_status not in ['member', 'administrator', 'creator']:
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel)
    if not_joined:
        text = "Please join the following channels:\n" + "\n".join(not_joined)
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=get_verification_keyboard()
        )
    else:
        mark_user_verified(user_id)
        add_user_log(user_id, "Verified")
        await query.answer("You are verified!")
        await query.edit_message_text(
            text="You are verified! Welcome to the main menu.",
            reply_markup=get_main_menu_keyboard()
        )

@error_handler
async def account_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Retrieves and displays the user's account information from the database.
    """
    query = update.callback_query
    user = get_user(query.from_user.id)
    if user:
        info = (
            f"Username: {user[1]}\n"
            f"User ID: {user[0]}\n"
            f"Role: {user[2]}\n"
            f"Joined: {user[3]}\n"
            f"Points: {user[5]}"
        )
    else:
        info = "User info not found."
    await query.answer()
    await query.edit_message_text(text=info, reply_markup=get_main_menu_keyboard())

@error_handler
async def referral_system_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays referral statistics (total referrals and earned points) for the user,
    and provides a button to get a referral link.
    """
    query = update.callback_query
    user_id = query.from_user.id
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*), COALESCE(SUM(points_earned), 0) FROM referrals WHERE referrer_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    total_refs = result[0] if result else 0
    total_points = result[1] if result else 0
    info = f"Referral System:\nTotal Referrals: {total_refs}\nEarned Points: {total_points}"
    keyboard = [
        [InlineKeyboardButton(text="Get Referral Link", callback_data="get_ref_link")],
        [InlineKeyboardButton(text="Back to Menu", callback_data="menu_main")]
    ]
    await query.answer()
    await query.edit_message_text(
        text=info,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@error_handler
async def get_referral_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generates and displays a referral link for the user.
    """
    query = update.callback_query
    # Replace 'YourBot' with your actual bot username.
    ref_link = f"http://t.me/ShadowRewardsBot?start=ref{query.from_user.id}"
    await query.answer("Referral Link Generated")
    await query.edit_message_text(
        text=f"Your Referral Link:\n{ref_link}",
        reply_markup=get_main_menu_keyboard()
    )

@error_handler
async def review_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to submit a review or suggestion.
    """
    query = update.callback_query
    await query.answer("Please send your review or suggestion as a text message.")
    context.user_data['awaiting_review'] = True
    await query.edit_message_text(text="Please type your review/suggestion:")

@error_handler
async def menu_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the admin panel if the user is an admin; otherwise denies access.
    """
    query = update.callback_query
    if not is_admin(query.from_user.id):
        await query.answer("Access prohibited.")
        return
    from admin_features import admin_menu
    await admin_menu(update, context)

@error_handler
async def menu_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns the user to the main menu.
    """
    query = update.callback_query
    await query.edit_message_text(text="Main Menu", reply_markup=get_main_menu_keyboard())

@error_handler
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Routes incoming callback queries (from inline buttons) to the appropriate handler.
    """
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
    """
    Processes text messages; if awaiting a review submission, captures it.
    """
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
    """
    Processes the /claim command to redeem a key. If valid and unclaimed, adds points to the user's balance.
    """
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
