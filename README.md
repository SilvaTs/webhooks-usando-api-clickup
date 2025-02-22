# Webhook Integration with ClickUp API

Este projeto implementa uma integração com a API do ClickUp para monitorar e processar eventos de tarefas em tempo real através de webhooks.

## Sobre

O projeto consiste em dois componentes principais:
- Um cliente Python para interagir com a API do ClickUp
- Um servidor FastAPI para processar webhooks recebidos

### Principais Funcionalidades
- Autenticação com a API do ClickUp
- Busca de detalhes de tarefas específicas
- Processamento de eventos via webhook
- Monitoramento de tarefas específicas
- Logging detalhado de eventos e respostas

## Requisitos

- Python 3.x
- FastAPI
- Uvicorn
- python-dotenv
- requests

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/webhooks-usando-api-clickup.git
cd webhooks-usando-api-clickup
```

# Webhook Integration with ClickUp API

Este projeto implementa uma integração com a API do ClickUp para monitorar e processar eventos de tarefas em tempo real através de webhooks.

## Sobre

O projeto consiste em dois componentes principais:
- Um cliente Python para interagir com a API do ClickUp
- Um servidor FastAPI para processar webhooks recebidos

### Principais Funcionalidades
- Autenticação com a API do ClickUp
- Busca de detalhes de tarefas específicas
- Processamento de eventos via webhook
- Monitoramento de tarefas específicas
- Logging detalhado de eventos e respostas

## Requisitos

- Python 3.x
- FastAPI
- Uvicorn
- python-dotenv
- requests

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/webhooks-usando-api-clickup.git
cd webhooks-usando-api-clickup
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` com:
```env
CLICKUP_API_TOKEN=seu_token_aqui
TASK_ID_TO_MONITOR=id_da_tarefa
```

## Uso

### Cliente ClickUp

Para usar o cliente da API:
```python
from create_webhook import ClickUpClient

client = ClickUpClient()
task_details = client.get_task_details()
```

### Servidor Webhook

Para iniciar o servidor:
```bash
python app.py
```

O servidor estará disponível em `http://localhost:8000` com os endpoints:
- `POST /webhook`: Recebe eventos do ClickUp
- `GET /health`: Endpoint de verificação de saúde

## Estrutura do Projeto

```
webhooks-usando-api-clickup/
├── create_webhook.py    # Cliente da API ClickUp
├── app.py              # Servidor FastAPI
├── .env               # Variáveis de ambiente
└── README.md          # Esta documentação
```

## Desenvolvimento

### Logs
O projeto utiliza logging configurado para mostrar:
- Status de autenticação
- Detalhes das requisições
- Eventos processados
- Erros e exceções

### Tratamento de Erros
- Validação de token de API
- Verificação de payload do webhook
- Tratamento de exceções HTTP
- Logging de erros detalhado

## Exemplos de Código

### create_webhook.py
```python
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
```

### app.py
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="ClickUp Webhook Processor")

TASK_ID_TO_MONITOR = os.getenv('TASK_ID_TO_MONITOR', "86a6u")
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
```
