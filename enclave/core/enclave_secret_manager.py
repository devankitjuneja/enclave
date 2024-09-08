import json
from enclave.shared.models.secret import Secret
from enclave.shared.models.secret_version import SecretVersion
from enclave.shared.database import with_db_session
from enclave.core.encryption import EncryptionFactory


class EnclaveSecretManager:
    def __init__(self, default_algorithm='AES-256-CBC'):
        self.default_algorithm = default_algorithm

    @with_db_session
    def create_secret(self, name, value, db_session=None):
        # Check if the secret already exists
        existing_secret = db_session.query(Secret).filter_by(name=name).first()
        if existing_secret:
            raise ValueError(f"Secret with name '{name}' already exists.")

        # Get encryption algorithm instance
        encryption_algo = EncryptionFactory.get_encryption_algorithm(self.default_algorithm)
        encryption_key = encryption_algo.generate_key()
        encrypted_value = encryption_algo.encrypt(json.dumps(value))
        iv = encryption_algo.iv

        # Create new Secret entry
        new_secret = Secret(name=name)
        db_session.add(new_secret)
        db_session.flush()  # Ensure the new secret ID is available

        # Create new SecretVersion entry
        new_secret_version = SecretVersion(
            secret_id=new_secret.id,
            encrypted_value=encrypted_value,
            encrypted_key=encryption_key,
            iv=iv,
            algorithm=self.default_algorithm,
            version=1  # First version for this secret
        )
        db_session.add(new_secret_version)

        # Set the active version of the secret to this first version
        new_secret.active_version = 1

        db_session.commit()

        return new_secret
