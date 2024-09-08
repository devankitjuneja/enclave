import base64
import json
from pydantic import BaseModel
from enclave.shared.models.secret import Secret
from enclave.shared.models.secret_version import SecretVersion
from enclave.shared.database import with_db_session
from enclave.core.encryption import EncryptionFactory

class SecretResponse(BaseModel):
    id: str
    name: str
    active_version: int
    secret_value: str
    algorithm: str

class SecretGetResponse(BaseModel):
    id: str
    name: str
    secret_value: str
    value: str
    version: int
    algorithm: str

class EnclaveSecretManager:
    def __init__(self, default_algorithm='AES-256-CBC'):
        self.default_algorithm = default_algorithm

    @with_db_session
    def create_secret(self, name, value, db_session=None) -> SecretResponse:
        # Check if the secret already exists
        existing_secret = db_session.query(Secret).filter_by(name=name).first()
        if existing_secret:
            raise ValueError(f"Secret with name '{name}' already exists.")

        encryption_algo = EncryptionFactory.get_encryption_algorithm(self.default_algorithm)()

        encrypted_value = base64.b64encode(encryption_algo.encrypt(json.dumps(value))).decode('utf-8')
        encryption_key = base64.b64encode(encryption_algo.key).decode('utf-8')
        iv = base64.b64encode(encryption_algo.iv).decode('utf-8')

        new_secret = Secret(name=name)
        db_session.add(new_secret)
        db_session.flush()

        # Create new SecretVersion entry
        new_secret_version = SecretVersion(
            secret_id=new_secret.id,
            encrypted_value=encrypted_value,
            encrypted_key=encryption_key,
            iv=iv,
            algorithm=self.default_algorithm,
            version=1
        )
        db_session.add(new_secret_version)

        new_secret.active_version = 1

        db_session.commit()

        return SecretResponse(
            id=new_secret.id,
            name=new_secret.name,
            active_version=new_secret.active_version,
            secret_value=value,
            algorithm=self.default_algorithm
        )

    @with_db_session
    def update_secret(self, name, value, db_session=None) -> SecretResponse:
        existing_secret = db_session.query(Secret).filter_by(name=name).first()
        if not existing_secret:
            raise ValueError(f"Secret with name '{name}' does not exist.")

        current_version = existing_secret.active_version
        new_version = current_version + 1

        encryption_algo = EncryptionFactory.get_encryption_algorithm(self.default_algorithm)()

        encrypted_value = base64.b64encode(encryption_algo.encrypt(json.dumps(value))).decode('utf-8')
        encryption_key = base64.b64encode(encryption_algo.key).decode('utf-8')
        iv = base64.b64encode(encryption_algo.iv).decode('utf-8')

        new_secret_version = SecretVersion(
            secret_id=existing_secret.id,
            encrypted_value=encrypted_value,
            encrypted_key=encryption_key,
            iv=iv,
            algorithm=self.default_algorithm,
            version=new_version
        )
        db_session.add(new_secret_version)

        existing_secret.active_version = new_version

        db_session.commit()

        return SecretResponse(
            id=existing_secret.id,
            name=existing_secret.name,
            active_version=existing_secret.active_version,
            secret_value=value,
            algorithm=self.default_algorithm
        )

    @with_db_session
    def get_secret(self, name, version=None, db_session=None):
        secret = db_session.query(Secret).filter_by(name=name).first()
        if not secret:
            raise ValueError(f"Secret with name '{name}' does not exist.")

        if version:
            secret_version = db_session.query(SecretVersion).filter_by(secret_id=secret.id, version=version).first()
            if not secret_version:
                raise ValueError(f"Version {version} for secret '{name}' does not exist.")
        else:
            secret_version = db_session.query(SecretVersion).filter_by(secret_id=secret.id, version=secret.active_version).first()

        if not secret_version:
            raise ValueError(f"No versions available for secret '{name}'.")

        encrypted_value = base64.b64decode(secret_version.encrypted_value)
        encryption_key = base64.b64decode(secret_version.encrypted_key)
        iv = base64.b64decode(secret_version.iv)

        encryption_algo = EncryptionFactory.get_encryption_algorithm(secret_version.algorithm)(encryption_key, iv)
        decrypted_value = encryption_algo.decrypt(encrypted_value)

        return SecretGetResponse(
            id=secret.id,
            name=secret.name,
            secret_value=secret_version.encrypted_value,
            value=decrypted_value,
            version=secret_version.version,
            algorithm=secret_version.algorithm
        )

    @with_db_session
    def delete_secret(self, name, db_session=None):
        # Fetch the secret by name
        secret = db_session.query(Secret).filter_by(name=name).first()
        if not secret:
            raise ValueError(f"Secret with name '{name}' does not exist.")

        db_session.delete(secret)
        db_session.commit()

        return f"Secret '{name}' deleted successfully."
