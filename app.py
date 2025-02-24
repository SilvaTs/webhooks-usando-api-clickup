from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="ClickUp Webhook Manager",
    description="API for managing ClickUp webhooks",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
if not CLICKUP_API_TOKEN:
    raise ValueError("CLICKUP_API_TOKEN environment variable is required")

class WebhookCreate(BaseModel):
    endpoint: str
    description: str = None

class Webhook(BaseModel):
    id: str
    endpoint: str
    client_id: str
    workspace_id: str
    user_id: str
    events: List[str]

class WebhookList(BaseModel):
    webhooks: List[Webhook]

@app.post("/team/{team_id}/webhook", response_model=Webhook, tags=["webhooks"],
    summary="Create a new webhook",
    description="Creates a new webhook for the specified team")
async def create_webhook(team_id: int, webhook: WebhookCreate):
    try:
        headers = {
            "Authorization": CLICKUP_API_TOKEN,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"https://api.clickup.com/api/v2/team/{team_id}/webhook",
            headers=headers,
            json={"endpoint": webhook.endpoint, "description": webhook.description}
        )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating webhook: {str(e)}")
        raise HTTPException(
            status_code=response.status_code if hasattr(response, 'status_code') else 500,
            detail=str(e)
        )

@app.get("/team/{team_id}/webhook", response_model=WebhookList, tags=["webhooks"],
    summary="List team webhooks",
    description="Retrieves all webhooks for the specified team")
async def get_webhooks(team_id: int):
    try:
        headers = {
            "Authorization": CLICKUP_API_TOKEN,
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"https://api.clickup.com/api/v2/team/{team_id}/webhook",
            headers=headers
        )
        
        response.raise_for_status()
        webhooks_data = response.json()
        return {"webhooks": webhooks_data.get("webhooks", [])}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving webhooks: {str(e)}")
        raise HTTPException(
            status_code=response.status_code if hasattr(response, 'status_code') else 500,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()
    
    uvicorn.run(app, host="0.0.0.0", port=args.port)