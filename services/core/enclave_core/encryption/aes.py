import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from enclave_core.encryption.base import EncryptionAlgorithm


class AESAlgorithm(EncryptionAlgorithm):
    def __init__(self, key: bytes, iv: bytes = None):
        self.key = key
        self.iv = iv or os.urandom(16)
        self.backend = default_backend()

    def generate_key(self):
        return os.urandom(32)  # 256-bit key

    def encrypt(self, plaintext: str) -> bytes:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return self.iv + ciphertext  # Prepend IV for use in decryption

    def decrypt(self, ciphertext: bytes) -> str:
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()
