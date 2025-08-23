from fastapi import FastAPI
import database

app = FastAPI()

app.include_router(database.router)