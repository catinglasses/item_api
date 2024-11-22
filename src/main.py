from fastapi import FastAPI
from v1.api import app as api_router

app = FastAPI()

app.include_router(api_router)

# Optional: You can define a root endpoint for testing
@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")