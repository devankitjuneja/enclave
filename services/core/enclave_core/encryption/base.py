# enclave/encryption/base.py

from abc import ABC, abstractmethod

class EncryptionAlgorithm(ABC):
    @abstractmethod
    def generate_key(self):
        pass

    @abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> str:
        pass
