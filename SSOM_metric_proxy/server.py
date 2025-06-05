from fastapi import FastAPI, Request
import httpx
import os
from json_parser import parse_alert_webhook
app = FastAPI()

TARGET_WEBHOOK_URLS = os.getenv("TARGET_WEBHOOK_URL", "")
WEBHOOK_URL_LIST = [url.strip() for url in TARGET_WEBHOOK_URLS.split(",") if url.strip()]

@app.post("/receive-alert-webhook")
async def receive_grafana_webhook(request: Request):
    data = await request.json()
    payload = parse_alert_webhook(data)
    sent_urls = []

    async with httpx.AsyncClient() as client:
        for url in WEBHOOK_URL_LIST:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            sent_urls.append(url)

    return {
        "isSuccess": True,
        "forwarded_urls": sent_urls
    }
