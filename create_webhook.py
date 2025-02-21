import requests
import os
from dotenv import load_dotenv
import logging
import json
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
logger.propagate = False

class ClickUpClient:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('CLICKUP_API_TOKEN')
        self.base_url = "https://api.clickup.com/api/v2"
        self.task_id = "86a6u6bck"
        
        if not self.api_token:
            raise ValueError("Missing CLICKUP_API_TOKEN in environment variables")

    def format_and_print_json(self, data, title):
        json_str = json.dumps(
            data,
            ensure_ascii=False,
            separators=(',', ':'),
            default=str
        )
        print(f"\n{title}:")
        print(json_str)
        print("-" * 80)

    def test_authentication(self):
        headers = {
            "Authorization": self.api_token,
            "accept": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/team",
                headers=headers
            )
            self.format_and_print_json(response.json(), "Resposta da autenticação")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Erro de autenticação: {e}")
            return False

    def get_task_details(self):
        headers = {
            "Authorization": self.api_token,
            "accept": "application/json"
        }

        try:
            response = requests.get(
                f"{self.base_url}/task/{self.task_id}",
                headers=headers
            )
            print(f"\nURL da requisição: {self.base_url}/task/{self.task_id}")
            print(f"Código de status da resposta: {response.status_code}")
            
            response.raise_for_status()
            task_data = response.json()
            
            self.format_and_print_json(task_data, "Detalhes completos da tarefa")
            return task_data

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes da tarefa: {e}")
            raise

if __name__ == "__main__":
    try:
        client = ClickUpClient()
        
        if not client.test_authentication():
            print("Falha na autenticação. Verifique seu token API.")
            exit(1)
            
        print("Autenticação bem sucedida. Buscando detalhes da tarefa...")
        task_details = client.get_task_details()
        client.format_and_print_json(task_details, "Detalhes da tarefa obtidos com sucesso")
    except Exception as e:
        print(f"Falha ao obter detalhes da tarefa: {e}")