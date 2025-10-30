from fastapi import FastAPI
import routers 

app = FastAPI(title="Order Service API")

app.include_router(routers.router)