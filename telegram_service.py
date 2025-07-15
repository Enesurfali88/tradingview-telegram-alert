import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class TelegramService:
    """Service class for handling Telegram bot interactions."""
    
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.user_id = Config.TELEGRAM_USER_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        """
        Send a message to the configured Telegram user.
        
        Args:
            message (str): The message to send
            
        Returns:
            dict: Response from Telegram API or error information
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.user_id,
                "text": message,
                "parse_mode": "HTML"  # Enable HTML formatting
            }
            
            logger.debug(f"Sending Telegram message to user {self.user_id}")
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("Message sent successfully to Telegram")
                return {"status": "success", "response": response.json()}
            else:
                logger.error(f"Failed to send Telegram message: {response.status_code} - {response.text}")
                return {"status": "error", "message": f"Telegram API error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception when sending Telegram message: {str(e)}")
            return {"status": "error", "message": f"Network error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error when sending Telegram message: {str(e)}")
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}
    
    def format_alert_message(self, alert_data):
        """
        Format the TradingView alert data into a readable message.
        
        Args:
            alert_data (dict): The alert data from TradingView
            
        Returns:
            str: Formatted message for Telegram
        """
        try:
            # Extract message from alert data
            message = alert_data.get("message", Config.DEFAULT_MESSAGE)
            
            # Add additional formatting if other fields are present
            formatted_message = f"{Config.MESSAGE_PREFIX}{message}"
            
            # Add extra information if available
            if "symbol" in alert_data:
                formatted_message += f"\n📊 Symbol: {alert_data['symbol']}"
            
            if "price" in alert_data:
                formatted_message += f"\n💰 Price: {alert_data['price']}"
            
            if "time" in alert_data:
                formatted_message += f"\n🕐 Time: {alert_data['time']}"
            
            return formatted_message
            
        except Exception as e:
            logger.error(f"Error formatting alert message: {str(e)}")
            return f"{Config.MESSAGE_PREFIX}{Config.DEFAULT_MESSAGE}"
