from enclave_core.encryption.aes import AESAlgorithm
from enclave_core.encryption.base import EncryptionAlgorithm


ENCRYPTION_ALGORITHMS = {
    'AES': AESAlgorithm,
}

class EncryptionFactory:
    @staticmethod
    def get_encryption_algorithm(algorithm_type: str) -> EncryptionAlgorithm:
        if algorithm_type == "AES":
            return AESAlgorithm
        else:
            raise ValueError(f"Unsupported algorithm type: {algorithm_type}")
