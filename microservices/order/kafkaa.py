from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import HTTPException
import json
import asyncio
import uuid

# handlers
pending_requests: dict[str, asyncio.Future] = {}

async def handle_auth_response(data: dict):
    correlation_id = data["correlation_id"]
    if correlation_id not in pending_requests:
        return

    future = pending_requests.pop(correlation_id)

    if data.get("error"):
        future.set_exception(
            HTTPException(
                status_code=data.get("status_code", 401),
                detail=data["error"]
            )
        )
    else:
        future.set_result(data["user_id"])

async def get_user_id_via_kafka(authorization_header: str) -> int:
    token = (authorization_header or "").strip()
    correlation_id = str(uuid.uuid4())

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending_requests[correlation_id] = future

    await send("auth_requests", {
        "correlation_id": correlation_id,
        "token": token,
    })

    try:
        return await asyncio.wait_for(future, timeout=5.0)
    except asyncio.TimeoutError:
        pending_requests.pop(correlation_id, None)
        raise HTTPException(status_code=504, detail="Auth service timeout")

#producer
producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    
async def stop_producer():
    if producer:
        await producer.stop()
        
async def send(topic: str, data: dict):
    payload = json.dumps(data).encode()
    await producer.send(topic, value=payload)
    
#consumer
async def listen_auth_responses():
    consumer = AIOKafkaConsumer(
        "auth_responses",
        bootstrap_servers="localhost:9092",
        group_id="order-service",
    )
    await consumer.start()
    async for msg in consumer:
        data = json.loads(msg.value)
        await handle_auth_response(data) 