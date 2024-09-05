from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, text, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Secret(Base):
    __tablename__ = 'secrets'

    id = Column(String(36), primary_key=True, index=True, nullable=False, server_default=text("uuid_generate_v4()"))
    version = Column(Integer, nullable=False, default=1)
    name = Column(text, nullable=False, unique=True)
    encryption_algorithm_id = Column(String(36), ForeignKey('encryption_algorithms.id'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    encryption_algorithm = relationship('EncryptionAlgorithm', foreign_keys=[encryption_algorithm_id])
