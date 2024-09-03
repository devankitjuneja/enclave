from sqlalchemy import Column, String, text
from .base import Base

class EncryptionAlgorithm(Base):
    __tablename__ = 'encryption_algorithms'

    id = Column(String(36), primary_key=True, index=True, nullable=False, server_default=text("uuid_generate_v4()"))
    name = Column(String, unique=True, nullable=False)
    description = Column(text)
