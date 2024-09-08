import pytest
from faker import Faker
from enclave.shared.models.secret import Secret
from enclave.shared.models.secret_version import SecretVersion
from enclave.core.enclave_secret_manager import EnclaveSecretManager

fake = Faker()

# Create the test for creating a secret
def test_create_secret_success(db_session):
    secret_manager = EnclaveSecretManager()

    # Generate fake data for testing
    secret_name = fake.unique.word()
    secret_value = fake.sentence()

    # Call the create_secret method
    new_secret = secret_manager.create_secret(name=secret_name, value=secret_value)

    # Check if the secret was created in the database
    created_secret = db_session.query(Secret).filter_by(name=secret_name).first()
    assert created_secret is not None
    assert created_secret.name == secret_name

    # Check if the associated secret version was created
    secret_version = db_session.query(SecretVersion).filter_by(secret_id=created_secret.id).first()
    assert secret_version is not None
    assert secret_version.version == 1
    assert secret_version.encrypted_value != secret_value  # Ensure the value is encrypted
    assert secret_version.algorithm == secret_manager.default_algorithm

def test_create_secret_duplicate():
    secret_manager = EnclaveSecretManager()

    # Generate fake data for testing
    secret_name = fake.unique.word()
    secret_value = fake.sentence()

    # Create the secret
    secret_manager.create_secret(name=secret_name, value=secret_value)

    with pytest.raises(ValueError):
        secret_manager.create_secret(name=secret_name, value=secret_value)

def test_update_secret(db_session):
    secret_manager = EnclaveSecretManager()

    # Step 1: Create a new secret
    secret_name = fake.unique.word()
    secret_value = fake.sentence()
    new_value = fake.sentence()

    created_secret = secret_manager.create_secret(name=secret_name, value=secret_value)

    # Step 2: Check that the secret was created correctly
    secret_in_db = db_session.query(Secret).filter_by(name=secret_name).first()
    assert secret_in_db is not None
    assert secret_in_db.name == secret_name
    assert secret_in_db.active_version == 1

    # Check that the version 1 is created in SecretVersion
    secret_version_in_db = db_session.query(SecretVersion).filter_by(secret_id=created_secret.id).first()
    assert secret_version_in_db is not None
    assert secret_version_in_db.version == 1

    # Step 3: Update the secret with a new value
    updated_secret = secret_manager.update_secret(name=secret_name, value=new_value)

    # Step 4: Check that the version number has incremented
    assert updated_secret.active_version == 2

    # Check that the new version (version 2) is added to SecretVersion
    new_version_in_db = db_session.query(SecretVersion).filter_by(secret_id=updated_secret.id, version=2).first()
    assert new_version_in_db is not None
    assert new_version_in_db.version == 2

    # Check that the new version contains the updated encrypted value
    assert new_version_in_db.encrypted_value != secret_version_in_db.encrypted_value  # Should be different as it's encrypted

def test_get_secret():
    secret_manager = EnclaveSecretManager()

    secret_name = fake.unique.word()

    # Create the secret
    secret_manager.create_secret(name=secret_name, value="This is a test message")


    # Fetch the latest version of the secret
    fetched_secret = secret_manager.get_secret(secret_name)

    assert fetched_secret.name == secret_name
    assert fetched_secret.version == 1

def test_get_specific_version():
    secret_manager = EnclaveSecretManager()
    secret_name = "affect"

    specific_version = 2
    fetched_secret = secret_manager.get_secret(secret_name, version=specific_version)

    assert fetched_secret.name == secret_name
    assert fetched_secret.version == specific_version

def test_delete_secret(db_session):
    enclave_secret_manager = EnclaveSecretManager()
    created_secret = enclave_secret_manager.create_secret("test_secret", "test_value")

    assert db_session.query(Secret).filter_by(name="test_secret").first() is not None

    result = enclave_secret_manager.delete_secret("test_secret")

    assert db_session.query(Secret).filter_by(name="test_secret").first() is None
    assert db_session.query(SecretVersion).filter_by(secret_id=created_secret.id).first() is None

    assert result == "Secret 'test_secret' deleted successfully."
