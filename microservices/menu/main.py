from fastapi import FastAPI
import database, add, menu, delete

app = FastAPI()

app.include_router(database.router)
app.include_router(add.router)
app.include_router(menu.router)
app.include_router(delete.router)