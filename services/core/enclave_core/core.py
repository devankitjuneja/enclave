# enclave/core.py

from shared.models.secret import Secret
from shared.models.secret_version import SecretVersion
from shared.models.encryption_algorithm import EncryptionAlgorithm
from services.core.database import with_db_session
from services.core.enclave_core.encryption import get_encryption_algorithm

class EnclaveSecretManager:
    def __init__(self, default_algorithm='AES'):
        self.default_algorithm = default_algorithm

    @with_db_session
    def create_secret(self, name, value, db_session=None):
        if db_session.query(SecretVersion).filter_by(name=name).first():
            raise ValueError(f"Secret with name '{name}' already exists.")

        algo = db_session.query(EncryptionAlgorithm).filter_by(name=self.default_algorithm).first()
        algorithm = get_encryption_algorithm(algo.name, key=algo.key)
        key = algorithm.generate_key()
        encrypted_value = algorithm.encrypt(value)

        secret = Secret(name=name)
        db_session.add(secret)
        db_session.flush()

        secret_version = SecretVersion(secret_id=secret.id, key=key, value=encrypted_value)