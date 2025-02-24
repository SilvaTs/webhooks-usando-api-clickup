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

# Store monitored task ID in memory
monitored_task_id = None

class WebhookProcessor:
    @staticmethod
    async def process_event(payload: Dict[Any, Any]) -> None:
        task_data = payload.get("task", {})
        event_type = payload.get("event")
        
        logger.info(f"Processing {event_type} event for task {task_data.get('id')}")

@app.get("/")
async def root():
    return {
        "message": "ClickUp Webhook API",
        "endpoints": {
            "/webhook": "POST - Receive ClickUp webhook events",
            "/health": "GET - Check API health status",
            "/configure/{task_id}": "POST - Configure task monitoring"
        }
    }

@app.post("/webhook")
async def webhook_listener(request: Request):
    try:
        payload = await request.json()
        
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        
        task_id = payload.get("task", {}).get("id")
        event_type = payload.get("event")

        if not task_id or not event_type:
            raise HTTPException(status_code=400, detail="Missing task ID or event type")

        if task_id == monitored_task_id:
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

@app.post("/configure/{task_id}")
async def configure_monitored_task(task_id: str):
    global monitored_task_id
    monitored_task_id = task_id
    logger.info(f"Now monitoring task: {task_id}")
    return {"status": "success", "monitored_task": task_id}

@app.get("/webhook")
async def webhook_get():
    raise HTTPException(
        status_code=405,
        detail="Method Not Allowed. Use POST for webhook events"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "monitored_task": monitored_task_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)