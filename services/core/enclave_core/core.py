from shared.models.secret import Secret
from shared.models.secret_version import SecretVersion
from shared.models.encryption_algorithm import EncryptionAlgorithm
from core.database import with_db_session
from enclave_core.encryption import EncryptionFactory


class EnclaveSecretManager:
    def __init__(self, default_algorithm='AES'):
        self.default_algorithm = default_algorithm

    @with_db_session
    def create_secret(self, name, value, db_session=None):
        if db_session.query(Secret).filter_by(name=name).first():
            raise ValueError(f"Secret with name '{name}' already exists.")

        el = db_session.query(EncryptionAlgorithm).filter_by(name=self.default_algorithm).first()
        algorithm = EncryptionFactory.get_encryption_algorithm(el.name)(el.key)
        key = algorithm.generate_key()
        encrypted_value = algorithm.encrypt(value)
