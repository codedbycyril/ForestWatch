# config.py
# Central place for all settings. Other files import Config from here.
import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

# Reads key=value lines from a file named .env (if it exists)
# and puts them into the environment.
load_dotenv()


class Config:
    # Configure a stable, random SECRET_KEY in the deployment environment.
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    RANGER_PASSWORD_HASH = os.getenv("RANGER_PASSWORD_HASH", "")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "").lower() in {
        "1", "true", "yes"
    }

    # Name of the SQLite database file (created in the project folder).
    DATABASE = os.getenv("DATABASE", "forestwatch.db")

    # The ranger phone that receives dispatch SMS alerts.
    RANGER_PHONE = os.getenv("RANGER_PHONE", "+254700000000")

    # Leave blank until an inbound SMS shortcode is assigned and configured.
    SMS_SHORTCODE = os.getenv("SMS_SHORTCODE", "")

    # Africa's Talking SMS credentials. If the key is empty,
    # the app simulates SMS instead of sending real ones.
    AT_USERNAME = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
    AT_API_KEY = os.getenv("AFRICASTALKING_API_KEY", "")
