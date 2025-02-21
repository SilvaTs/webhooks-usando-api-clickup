import requests
import os
from dotenv import load_dotenv
import logging
import json
import sys

# Configurar o logger para mostrar mensagens completas
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout  # Usar stdout para evitar truncamento
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
        """Função auxiliar para formatar e imprimir JSON completo"""
        formatted_json = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            separators=(',', ': '),
            default=str
        )
        print(f"\n{title}:")
        print(formatted_json)
        print("-" * 80)  # Separador para melhor legibilidade

    def get_task_details(self):
        """Get details of a specific task"""
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
            
            # Usar a nova função para garantir exibição completa
            self.format_and_print_json(task_data, "Detalhes completos da tarefa")
            return task_data

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes da tarefa: {e}")
            raise

if __name__ == "__main__":
    try:
        client = ClickUpClient()
        
        if not client.test_authentication():
            logger.error("Falha na autenticação. Verifique seu token API.")
            exit(1)
            
        logger.info("Autenticação bem sucedida. Buscando detalhes da tarefa...")
        task_details = client.get_task_details()
        # Não precisamos logar novamente aqui pois já foi exibido em get_task_details
    except Exception as e:
        logger.error(f"Falha ao obter detalhes da tarefa: {e}")
        # Formatando o último log também
        formatted_details = json.dumps(task_details, indent=2, ensure_ascii=False, separators=(',', ': '))
        logger.info(f"Detalhes da tarefa obtidos com sucesso:\n{formatted_details}")
    except Exception as e:
        logger.error(f"Falha ao obter detalhes da tarefa: {e}")