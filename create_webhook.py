import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpClient:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('CLICKUP_API_TOKEN')
        self.base_url = "https://api.clickup.com/api/v2"
        self.task_id = "86a6u6bck"  # Specific task ID
        
        if not self.api_token:
            raise ValueError("Missing CLICKUP_API_TOKEN in environment variables")

    def get_task_details(self):
        """Get details of a specific task"""
        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(
                f"{self.base_url}/task/{self.task_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching task details: {e}")
            raise

if __name__ == "__main__":
    try:
        client = ClickUpClient()
        task_details = client.get_task_details()
        logger.info(f"Task details retrieved successfully: {task_details}")
    except Exception as e:
        logger.error(f"Failed to get task details: {e}")