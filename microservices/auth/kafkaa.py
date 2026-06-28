from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from dotenv import load_dotenv
import asyncio, json, os
from login import validate_token_from_kafka
from database import SessionLocal


load_dotenv()

producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()

async def stop_producer():
    if producer:
        await producer.stop()

async def send(topic: str, data: dict):
    payload = json.dumps(data).encode()
    await producer.send(topic, value=payload)

async def listen_auth_requests():
    consumer = AIOKafkaConsumer(
        "auth_requests",
        bootstrap_servers="kafka:9092",
        group_id="auth-service",
    )
    await consumer.start()
    async for msg in consumer:
        data = json.loads(msg.value)
        print(f"[AUTH] received: {data}")
        await handle_auth_request(data)

from database import SessionLocal

async def handle_auth_request(data: dict):
    correlation_id = data["correlation_id"]
    token = data["token"]

    try:
        async with SessionLocal() as session:
            user_id = await validate_token_from_kafka(token, session)
        await send("auth_responses", {
            "correlation_id": correlation_id,
            "user_id": user_id,
        })
    except Exception as e:
        print(f"[AUTH] failed: {e}")
        await send("auth_responses", {
            "correlation_id": correlation_id,
            "user_id": None,
            "error": "Ошибка аутентификации",
            "status_code": 401,
        })