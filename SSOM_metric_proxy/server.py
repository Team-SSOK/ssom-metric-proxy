from fastapi import FastAPI, Request
import httpx
import os
from json_parser import parse_alert_webhook
app = FastAPI()

TARGET_WEBHOOK_URL = os.getenv("TARGET_WEBHOOK_URL")

@app.post("/receive-alert-webhook")
async def receive_grafana_webhook(request: Request):
    data = await request.json()
    payload = parse_alert_webhook(data)

    async with httpx.AsyncClient() as client:
        response = await client.post(TARGET_WEBHOOK_URL, json=payload)
        response.raise_for_status()

    return {"sent": True, "forwarded_count": len(payload.get("alerts", []))}
