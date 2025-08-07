from fastapi import FastAPI
import register, database, login

app = FastAPI()

app.include_router(register.router)
app.include_router(database.router)
app.include_router(login.router)
