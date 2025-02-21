import requests
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpClient:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('CLICKUP_API_TOKEN')
        self.base_url = "https://api.clickup.com/api/v2"
        self.task_id = "86a6u6bck"
        
        if not self.api_token:
            raise ValueError("Missing CLICKUP_API_TOKEN in environment variables")

    def test_authentication(self):
        """Test if the API token is valid"""
        headers = {
            "Authorization": f"Bearer {self.api_token}",  # Add Bearer prefix
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/team",
                headers=headers
            )
            logger.info(f"Auth Response Status: {response.status_code}")
            logger.info(f"Auth Response: {response.text}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication error: {e}")
            return False

    def get_task_details(self):
        """Get details of a specific task"""
        headers = {
            "Authorization": f"Bearer {self.api_token}",  # Add Bearer prefix
            "Content-Type": "application/json"
        }

        try:
            # First, verify authentication by testing team access
            test_response = requests.get(
                f"{self.base_url}/team",
                headers=headers
            )
            logger.info(f"Authentication test status code: {test_response.status_code}")
            
            if test_response.status_code == 401:
                logger.error("Authentication failed. Please check your API token.")
                raise ValueError("Invalid API token")

            # If authentication successful, proceed with task details
            response = requests.get(
                f"{self.base_url}/task/{self.task_id}",
                headers=headers
            )
            logger.info(f"Request URL: {self.base_url}/task/{self.task_id}")
            logger.info(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching task details: {e}")
            raise

if __name__ == "__main__":
    try:
        client = ClickUpClient()
        
        # Test authentication first
        if not client.test_authentication():
            logger.error("Authentication failed. Please verify your API token.")
            exit(1)
            
        logger.info("Authentication successful. Proceeding with task details...")
        task_details = client.get_task_details()
        logger.info(f"Task details retrieved successfully: {task_details}")
    except Exception as e:
        logger.error(f"Failed to get task details: {e}")