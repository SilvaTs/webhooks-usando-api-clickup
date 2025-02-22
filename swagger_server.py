from flask import Flask, send_from_directory
import yaml
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Load YAML file
with open('api-docs.yaml', 'r', encoding='utf-8') as file:
    swagger_data = yaml.safe_load(file)

# Configure Swagger UI
SWAGGER_URL = '/api-docs'
API_URL = '/static/api-docs.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ClickUp API Documentation"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/api-docs.yaml')
def send_yaml():
    return send_from_directory('.', 'api-docs.yaml')

if __name__ == '__main__':
    app.run(port=3000, debug=True)