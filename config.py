# config.py
import os

# Bot token (set via an environment variable or directly here)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8017553859:AAHacxJhRk97GtKI8rNhjoXht_xh77kwiiQ")

# Channels required for verification (the bot must be admin in these channels)
REQUIRED_CHANNELS = [
    '@shadowsquad0',
    '@Originlabs',
    '@ShadowsquadHits',
    '@Binhub_Originlabs'
]

# Notification channel where scheduled messages are sent
NOTIFICATION_CHANNEL = '@shadowsquad0'

# Default owner IDs (replace these with actual Telegram user IDs of your bot owners)
DEFAULT_OWNERS = [7436974867, 7218606355, 5933410316, 5822279535]

# Banner image URL used across messages for a consistent, attractive look
BANNER_URL = "https://i.imgur.com/mDAjGNm.jpeg"
