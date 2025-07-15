import os
import logging
from flask import Flask, request, jsonify
from telegram_service import TelegramService
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize Telegram service
telegram_service = TelegramService()

@app.route("/", methods=["POST"])
def webhook():
    """
    TradingView webhook endpoint.
    Receives POST requests from TradingView and forwards alerts to Telegram.
    """
    try:
        # Log incoming request
        logger.debug(f"Received webhook request from {request.remote_addr}")
        
        # Check if request contains JSON data
        if not request.is_json:
            logger.warning("Request does not contain JSON data")
            return jsonify({
                "status": "error", 
                "message": "Content-Type must be application/json"
            }), 400
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            logger.warning("No JSON data received in request")
            return jsonify({
                "status": "error", 
                "message": "No JSON data received"
            }), 400
        
        logger.info(f"Processing TradingView alert: {data}")
        
        # Format the alert message
        formatted_message = telegram_service.format_alert_message(data)
        
        # Send message to Telegram
        telegram_result = telegram_service.send_message(formatted_message)
        
        if telegram_result["status"] == "success":
            logger.info("Alert successfully forwarded to Telegram")
            return jsonify({
                "status": "ok",
                "message": "Alert forwarded successfully"
            }), 200
        else:
            logger.error(f"Failed to forward alert to Telegram: {telegram_result['message']}")
            return jsonify({
                "status": "error",
                "message": "Failed to forward alert to Telegram",
                "details": telegram_result["message"]
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return jsonify({
        "status": "ok",
        "message": "TradingView webhook service is running"
    }), 200

@app.route("/test", methods=["POST"])
def test_telegram():
    """
    Test endpoint to verify Telegram integration.
    """
    try:
        test_message = "🧪 Test message from TradingView webhook service"
        result = telegram_service.send_message(test_message)
        
        if result["status"] == "success":
            return jsonify({
                "status": "ok",
                "message": "Test message sent successfully"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to send test message",
                "details": result["message"]
            }), 500
            
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "status": "error",
        "message": "Method not allowed"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == "__main__":
    logger.info("Starting TradingView webhook service...")
    logger.info(f"Service will be available at http://{Config.HOST}:{Config.PORT}")
    logger.info("Main webhook endpoint: POST /")
    logger.info("Health check endpoint: GET /health")
    logger.info("Test endpoint: POST /test")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
