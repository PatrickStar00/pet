from fastapi import FastAPI
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import routers 
import asyncio
from kafkaa import start_producer, stop_producer, listen_auth_responses

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer()
    task = asyncio.create_task(listen_auth_responses())
    yield
    task.cancel()
    await stop_producer()
    
app = FastAPI(lifespan=lifespan, title="Order Service API")

app.include_router(routers.router)