import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from enclave.api.routes import secrets

app = FastAPI()

API_KEY_NAME = "X-API-KEY"
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403, detail="Could not validate API key"
        )
    return api_key

app.include_router(secrets.router, dependencies=[Depends(get_api_key)])

# Root endpoint to verify API is running
@app.get("/")
async def root():
    return {"message": "Secret Manager API is running"}
