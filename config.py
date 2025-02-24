import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
CLICKUP_API_BASE_URL = "https://api.clickup.com/api/v2"
CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_SWAGGER_PORT = 3000

# Logging Configuration
LOG_FORMAT = '%(message)s'
API_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Connection Pool Configuration
MAX_CONNECTIONS = 10

# API Documentation
API_TITLE = "ClickUp Webhook Manager"
API_DESCRIPTION = "API for managing ClickUp webhooks"
API_VERSION = "1.0.0"