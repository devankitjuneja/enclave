from fastapi import FastAPI
from enclave.api.routes import secrets

app = FastAPI()

# Include the secrets router
app.include_router(secrets.router)

# Root endpoint to verify API is running
@app.get("/")
async def root():
    return {"message": "Secret Manager API is running"}
