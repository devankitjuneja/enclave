from sqlalchemy import (
    Column, String, Integer,
    ForeignKey, Text, DateTime,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enclave.shared.models import Base

class SecretVersion(Base):
    __tablename__ = 'secret_versions'

    id = Column(String(36), primary_key=True, index=True, nullable=False, server_default=text("uuid_generate_v4()"))
    secret_id = Column(String(36), ForeignKey('secrets.id'), nullable=False)
    encrypted_value = Column(Text, nullable=False)
    encrypted_key = Column(Text, nullable=False)
    iv = Column(Text, nullable=False)
    algorithm = Column(String(255), nullable=False)
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    secret = relationship("Secret", back_populates="secret_versions")
