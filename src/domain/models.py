from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema": None}  # ← importante para el translate_map

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default="seller", index=True)
    institution_name = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    full_name = Column(String(255), nullable=True)
    document_type = Column(String(50), nullable=True)
    document_number = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    telephone = Column(String(50), nullable=True)

class RefreshToken(Base):
    __tablename__ = "refresh_token"
    __table_args__ = {"schema": None}
    id = Column(Integer, primary_key=True)
    jti = Column(String(64), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)