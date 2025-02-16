# config.py
import os

# Bot token – either set via an environment variable or directly here.
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7760154469:AAHUQ_a6ODMubGpY9bqxVa2NqIvXCF2IWiE")

# Required channels for verification (the bot must be admin in these channels).
REQUIRED_CHANNELS = [
    '@shadowsquad0',
    '@Originlabs',
    '@ShadowsquadHits',
    '@Binhub_Originlabs'
]

# Notification channel where scheduled messages are sent.
NOTIFICATION_CHANNEL = '@shadowsquad0'

# Default owner IDs – replace with the actual Telegram user IDs of your bot owners.
DEFAULT_OWNERS = [7436974867, 7218606355, 5933410316, 5822279535]  # Example: [7436974867, 7218606355]

# Banner image URL for all messages.
BANNER_URL = "https://i.imgur.com/mDAjGNm.jpeg"
