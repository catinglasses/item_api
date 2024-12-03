from fastapi import FastAPI
from v1.api import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}
