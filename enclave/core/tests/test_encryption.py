import os
import pytest
from enclave.core.encryption import EncryptionFactory
from enclave.core.encryption.aes import AESAlgorithm


def test_aes_encrypt_decrypt():
    key = os.urandom(32)  # 256-bit AES key

    aes = EncryptionFactory.get_encryption_algorithm("AES")(key)

    json_data = {
        "key": "value"
    }
    plaintext = str(json_data)

    ciphertext = aes.encrypt(plaintext)
    assert ciphertext != b'', "Ciphertext should not be empty"

    decrypted_text = aes.decrypt(ciphertext)
    assert decrypted_text == plaintext, "Decrypted text should match the original plaintext"


def test_aes_different_iv():
    key = os.urandom(32)  # 256-bit AES key
    plaintext = "This is a test message"

    aes1 = EncryptionFactory.get_encryption_algorithm("AES")(key)
    key = os.urandom(32)
    aes2 = EncryptionFactory.get_encryption_algorithm("AES")(key)

    ciphertext1 = aes1.encrypt(plaintext)
    ciphertext2 = aes2.encrypt(plaintext)

    assert ciphertext1 != ciphertext2, "Ciphertexts should be different for different IVs"

def test_aes_generate_key():
    aes = EncryptionFactory.get_encryption_algorithm("AES")(os.urandom(32))
    generated_key = aes.generate_key()

    assert len(generated_key) == 32, "Generated key should be 256 bits long (32 bytes)"

def test_factory_returns_aes_algorithm():
    key = os.urandom(32)  # 256-bit AES key

    # Initialize AESAlgorithm using the factory
    aes = EncryptionFactory.get_encryption_algorithm("AES")
    aes_instance = aes(key)

    assert isinstance(aes_instance, AESAlgorithm), "Factory should return an AESAlgorithm instance"

def test_diff_encypt_decrypt_key():
    key = os.urandom(32)  # 256-bit AES key
    aes = EncryptionFactory.get_encryption_algorithm("AES")(key)

    json_data = {
        "key": "value"
    }
    plaintext = str(json_data)

    ciphertext = aes.encrypt(plaintext)
    assert ciphertext != b'', "Ciphertext should not be empty"

    key = os.urandom(32)
    aes = EncryptionFactory.get_encryption_algorithm("AES")(key)

    decrypted_text = aes.decrypt(ciphertext)
    assert decrypted_text != plaintext, "Decrypted text should not match the original plaintext"
