import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_URL = os.environ.get('SQLALCHEMY_URI')

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a fixture for a database session
@pytest.fixture(scope='function')
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope='function')
def test_data():
    yield {
        "ciphertext": "sDrC76j5JKFIVvHAhshXmZT+soPe7937uCYGDv9W4WbuDXAr8WSwdIavwqlWDwpS",
        "expected_plaintext": "This is a test message",
        "key": "LUbW0MFi02uGXDLX1ApKIeTSs/bt1bVlfTUk8qRG8iA=",
        "iv": "sDrC76j5JKFIVvHAhshXmQ=="
    }