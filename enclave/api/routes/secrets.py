import json
from typing import List
from fastapi import (
    APIRouter, HTTPException,
    Query, Depends
)
from loguru import logger
from sqlalchemy.orm import joinedload
from enclave.shared.models.secret import Secret
from enclave.shared.models.secret_version import SecretVersion
from enclave.core.enclave_secret_manager import EnclaveSecretManager
from enclave.shared.database import get_db
from enclave.shared.redis_client import redis_client
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

class SecretVersionResponse(BaseModel):
    id: str
    version: int
    encrypted_value: str
    algorithm: str

    class Config:
        orm_mode = True

class SecretListResponse(BaseModel):
    id: str
    name: str
    active_version: int
    created_at: str
    updated_at: str
    secret_versions: List[SecretVersionResponse]

    class Config:
        orm_mode = True

@router.get("/list", response_model=List[SecretListResponse])
async def list_secrets(
    db=Depends(get_db)
) -> List[SecretListResponse]:
    try:
        secrets = db.query(Secret).options(
            joinedload(Secret.secret_versions)
        ).all()

        # Map secrets and versions to SecretResponse and SecretVersionResponse models
        secret_responses = [
            SecretListResponse(
                id=secret.id,
                name=secret.name,
                active_version=secret.active_version,
                created_at=str(secret.created_at),
                updated_at=str(secret.updated_at),
                secret_versions=[
                    SecretVersionResponse(
                        id=version.id,
                        version=version.version,
                        encrypted_value=version.encrypted_value,
                        algorithm=version.algorithm
                    ) for version in secret.secret_versions
                ]
            ) for secret in secrets
        ]

        return secret_responses
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


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
    # If version is not provided, fetch the active version
    if version is None:
        version = secret_manager.get_active_version(secret_id=secret_id)

    redis_key = f"secret:{secret_id}:version:{version}"

    cached_secret = redis_client.get(redis_key)

    if cached_secret:
        logger.info(f"Cache hit for secret {secret_id} version {version}")
        return SecretResponse(**json.loads(cached_secret))
        # return json.loads(cached_secret)

    # Otherwise, fetch the secret and cache it
    try:
        secret = secret_manager.get_secret(name=secret_id, version=version)
        secret_response = SecretResponse(
            id=secret.id, name=secret.name,
            version=secret.version,
            secret_value=secret.secret_value,
            value=secret.value
        )

        redis_client.setex(redis_key, 600, secret_response.model_dump_json())

        return secret_response
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
