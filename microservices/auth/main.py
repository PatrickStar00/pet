from fastapi import FastAPI
import register, database, login
from contextlib import asynccontextmanager
from kafkaa import start_producer, listen_auth_requests, stop_producer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer()
    task = asyncio.create_task(listen_auth_requests())
    yield
    task.cancel()
    await stop_producer()

app = FastAPI(lifespan=lifespan)

app.include_router(register.router)
app.include_router(database.router)
app.include_router(login.router)