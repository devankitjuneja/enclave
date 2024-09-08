from enclave.core.encryption.aes import AESAlgorithm
from enclave.core.encryption.base import EncryptionAlgorithm


ENCRYPTION_ALGORITHMS = {
    'AES-256-CBC': AESAlgorithm,
}

class EncryptionFactory:
    @staticmethod
    def get_encryption_algorithm(algorithm_type: str) -> EncryptionAlgorithm:
        return ENCRYPTION_ALGORITHMS[algorithm_type]
