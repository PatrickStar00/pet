from fastapi import FastAPI
import database, add

app = FastAPI()

app.include_router(database.router)
app.include_router(add.router)
