import os

class Config:
    """Configuration class for the TradingView webhook service."""
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7640770446:AAGVXrN_223yiYdfokqiyrpDNMQ2lNDNdNI")
    TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID", "142598365")
    
    # Flask Configuration
    SECRET_KEY = os.getenv("SESSION_SECRET", "your-secret-key-here")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", "8000"))
    
    # Message Configuration
    DEFAULT_MESSAGE = "📈 تنبيه جديد من TradingView 🚨"
    MESSAGE_PREFIX = "🚨 TradingView Alert:\n"
