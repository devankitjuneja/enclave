# enclave/encryption/__init__.py

from .aes import AESAlgorithm

ENCRYPTION_ALGORITHMS = {
    'AES': AESAlgorithm,
}

def get_encryption_algorithm(name: str, **kwargs):
    algorithm_class = ENCRYPTION_ALGORITHMS.get(name)
    if not algorithm_class:
        raise ValueError(f"Unsupported encryption algorithm: {name}")
    return algorithm_class(**kwargs)
