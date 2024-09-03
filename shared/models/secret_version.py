from sqlalchemy import Column, String, Integer, ForeignKey, text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class SecretVersion(Base):
    __tablename__ = 'secret_versions'

    id = Column(String(36), primary_key=True, index=True, nullable=False, server_default=text("uuid_generate_v4()"))
    version = Column(Integer, nullable=False, default=1)
    key = Column(text, nullable=False)
    value = Column(text, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    secret_id = Column(String(36), ForeignKey('secrets.id'))
