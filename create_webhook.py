import requests
import os
from dotenv import load_dotenv
import logging
import json

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
            "Authorization": self.api_token,
            "accept": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/team",
                headers=headers
            )
            logger.info(f"Código de status da autenticação: {response.status_code}")
            # Formatando o JSON com aspas duplas e indentação
            formatted_json = json.dumps(response.json(), indent=2, ensure_ascii=False, separators=(',', ': '))
            logger.info(f"Resposta da autenticação:\n{formatted_json}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de autenticação: {e}")
            return False

    def get_task_details(self):
        """Get details of a specific task"""
        headers = {
            "Authorization": self.api_token,
            "accept": "application/json"
        }

        try:
            # Verificação de autenticação
            test_response = requests.get(
                f"{self.base_url}/team",
                headers=headers
            )
            logger.info(f"Código de status da autenticação: {test_response.status_code}")
            
            if test_response.status_code == 401:
                logger.error("Falha na autenticação. Verifique seu token API.")
                raise ValueError("Token API inválido")

            # Buscar detalhes da tarefa
            response = requests.get(
                f"{self.base_url}/task/{self.task_id}",
                headers=headers
            )
            logger.info(f"URL da requisição: {self.base_url}/task/{self.task_id}")
            logger.info(f"Código de status da resposta: {response.status_code}")
            
            response.raise_for_status()
            # Formatando o JSON com aspas duplas e indentação correta
            formatted_json = json.dumps(response.json(), indent=2, ensure_ascii=False, separators=(',', ': '))
            logger.info(f"Detalhes da tarefa:\n{formatted_json}")
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