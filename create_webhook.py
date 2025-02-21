import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpWebhook:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('CLICKUP_API_TOKEN')
        self.team_id = os.getenv('TEAM_ID', '9013340838')
        self.webhook_url = os.getenv('WEBHOOK_URL')
        self.base_url = "https://api.clickup.com/api/v2"
        
    def create_webhook(self):
        if not all([self.api_token, self.team_id, self.webhook_url]):
            raise ValueError("Missing required environment variables")

        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }
        
        data = {
            "endpoint": self.webhook_url,
            "events": ["taskUpdated"],
            "health_check": True
        }

        try:
            response = requests.post(
                f"{self.base_url}/team/{self.team_id}/webhook",
                json=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating webhook: {e}")
            raise

if __name__ == "__main__":
    try:
        webhook = ClickUpWebhook()
        result = webhook.create_webhook()
        logger.info(f"Webhook created successfully: {result}")
    except Exception as e:
        logger.error(f"Failed to create webhook: {e}")