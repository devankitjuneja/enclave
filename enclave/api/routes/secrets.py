from fastapi import (
    APIRouter, HTTPException,
    Query
)
from enclave.core.enclave_secret_manager import EnclaveSecretManager
from pydantic import BaseModel

router = APIRouter(
    prefix="/secrets",
    tags=["secrets"],
    responses={404: {"description": "Not found"}},
)

secret_manager = EnclaveSecretManager()


class CreateSecretRequest(BaseModel):
    name: str
    value: str


class UpdateSecretRequest(BaseModel):
    value: str


class SecretResponse(BaseModel):
    id: str
    name: str
    version: int
    secret_value: str
    value: str


# Create a new secret
@router.post("", response_model=SecretResponse)
async def create_secret(request: CreateSecretRequest):
    try:
        secret = secret_manager.create_secret(
            name=request.name, value=request.value)
        return SecretResponse(
            id=secret.id, name=secret.name,
            version=secret.active_version,
            secret_value=secret.secret_value,
            value=secret.value
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update an existing secret
@router.put("/{secret_id}", response_model=SecretResponse)
async def update_secret(secret_id: str, request: UpdateSecretRequest):
    try:
        secret = secret_manager.update_secret(
            name=secret_id, value=request.value)
        return SecretResponse(
            id=secret.id, name=secret.name,
            version=secret.active_version,
            secret_value=secret.secret_value,
            value=secret.value
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Get a secret by ID
@router.get("/{secret_id}", response_model=SecretResponse)
async def get_secret(
    secret_id: str,
    version: int = Query(None, description="The version of the secret to fetch")
):
    try:
        secret = secret_manager.get_secret(name=secret_id, version=version)
        return SecretResponse(
            id=secret.id, name=secret.name,
            version=secret.version,
            secret_value=secret.secret_value,
            value=secret.value
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Delete a secret by ID
@router.delete("/{secret_id}")
async def delete_secret(secret_id: str):
    try:
        secret_manager.delete_secret(secret_id=secret_id)
        return {"message": "Secret deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
