from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="ClickUp Webhook Processor")

# Get task ID from environment variable or use default
TASK_ID_TO_MONITOR = os.getenv('TASK_ID_TO_MONITOR', "86a6u6bck")

class WebhookProcessor:
    @staticmethod
    async def process_event(payload: Dict[Any, Any]) -> None:
        """Process the webhook event"""
        task_data = payload.get("task", {})
        event_type = payload.get("event")
        
        logger.info(f"Processing {event_type} event for task {task_data.get('id')}")
        # Add your event processing logic here
        # For example: updating database, sending notifications, etc.

@app.post("/webhook")
async def webhook_listener(request: Request):
    try:
        payload = await request.json()
        
        # Validate payload
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        
        task_id = payload.get("task", {}).get("id")
        event_type = payload.get("event")

        if not task_id or not event_type:
            raise HTTPException(status_code=400, detail="Missing task ID or event type")

        if task_id == TASK_ID_TO_MONITOR:
            await WebhookProcessor.process_event(payload)
            logger.info(f"Successfully processed {event_type} event for task {task_id}")
            return JSONResponse(
                content={
                    "status": "success",
                    "message": f"Event {event_type} processed for task {task_id}"
                }
            )
        
        return JSONResponse(
            content={
                "status": "skipped",
                "message": "Event not for monitored task"
            }
        )

    except HTTPException as he:
        logger.error(f"HTTP Error: {str(he)}")
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)