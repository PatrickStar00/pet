from fastapi import FastAPI, Request, Body
import httpx
from dotenv import load_dotenv
import os
from typing import Optional
from urllib.parse import unquote


app = FastAPI()

load_dotenv()
SERVICES = {
    "auth" : os.getenv("AUTH_URL"),
    "menu" : os.getenv("MENU_URL"),
    "order" : os.getenv("ORDER_URL"),
}

@app.get("/{service}/{path:path}")
async def proxy_get(service: str, path: str, request: Request):
    return await proxy_request(service, path, request)

@app.post("/{service}/{path:path}")
async def proxy_post(service: str, path: str, request: Request, body: Optional[dict] = Body(None)):
    return await proxy_request(service, path, request)

@app.delete("/{service}/{path:path}")
async def proxy_delete(service: str, path: str, request: Request, body: Optional[dict] = Body(None)):
    return await proxy_request(service, path, request)

async def proxy_request(
    service: str, 
    path: str, 
    request: Request
    ):
    if service not in SERVICES:
        return {"error": "Unknown service"}

    decoded_path = unquote(path)
    
    target_url = f"{SERVICES[service]}/{decoded_path}"
    
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method, 
            target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

    return response.json()