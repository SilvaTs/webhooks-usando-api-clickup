# Webhook Integração com API ClickUp 

Este projeto implementa uma integração com a API do ClickUp para monitorar e processar eventos de tarefas em tempo real através de webhooks.

## Sobre

O projeto consiste em três componentes principais:
- Um cliente Python para interagir com a API do ClickUp
- Um servidor FastAPI para processar webhooks recebidos
- Documentação Swagger/OpenAPI para a API

### Principais Funcionalidades
- Autenticação com a API do ClickUp
- Busca de detalhes de tarefas específicas
- Processamento de eventos via webhook
- Monitoramento de tarefas específicas
- Documentação interativa via Swagger UI
- Logging detalhado de eventos e respostas

## Requisitos

- Python 3.x
- FastAPI
- Uvicorn
- python-dotenv
- requests
- flask
- flask-swagger-ui
- pyyaml

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SilvaTs/webhooks-usando-api-clickup.git
cd webhooks-usando-api-clickup
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a Aplicação

### 1. Cliente ClickUp

Para usar o cliente da API:
```python
from create_webhook import ClickUpClient

client = ClickUpClient()
task_details = client.get_task_details()
```

### 2. Documentação Swagger

1. Inicie o servidor Swagger:
```bash
python swagger_server.py
```

2. Acesse a documentação no navegador:
```
http://localhost:3000/api-docs
```

Na interface do Swagger UI você pode:
- Visualizar todos os endpoints disponíveis
- Testar as requisições
- Explorar os modelos de dados
- Ver exemplos de requisições e respostas

## Estrutura do Projeto

```
webhooks-usando-api-clickup/
├── create_webhook.py    # Cliente da API ClickUp
├── app.py              # Servidor FastAPI
├── swagger_server.py   # Servidor da documentação Swagger
├── api-docs.yaml      # Especificação OpenAPI/Swagger
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

## Troubleshooting

### Problemas Comuns

1. **Erro ao Iniciar o Swagger**
   - Verifique se todas as dependências estão instaladas
   - Confirme se a porta 3000 está disponível
   - Certifique-se que o arquivo api-docs.yaml existe no diretório

2. **Servidor não Inicia**
   - Confirme que todas as portas necessárias estão livres
   - Verifique se o Python 3.x está instalado corretamente
   - Confirme que todas as dependências foram instaladas

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
