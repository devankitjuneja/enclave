from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, text
from sqlalchemy.orm import relationship
from enclave.shared.models import Base

class Secret(Base):
    __tablename__ = 'secrets'

    id = Column(String(36), primary_key=True, index=True, nullable=False, server_default=text("uuid_generate_v4()"))
    name = Column(Text, nullable=False, unique=True)
    active_version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    secret_versions = relationship("SecretVersion", back_populates="secret")
