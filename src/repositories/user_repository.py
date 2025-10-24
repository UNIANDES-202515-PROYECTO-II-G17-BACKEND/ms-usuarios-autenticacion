from typing import Optional, List
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.domain.models import Usuario, RefreshToken




class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_users(self, role: Optional[str] = None, offset: int = 0, limit: int = 100) -> List[Usuario]:
        stmt = select(Usuario)
        if role:
            stmt = stmt.where(Usuario.role == role)
        stmt = stmt.offset(offset).limit(limit)
        return self.session.execute(stmt).scalars().all()

    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.session.execute(
            select(Usuario).where(Usuario.username == username)
        ).scalar_one_or_none()


    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        return self.session.get(Usuario, user_id)


    def create_user(self, username: str, password_hash: str, role: str = "seller", institution_name: str | None = None, full_name: str | None = None, document_type: str | None = None, document_number: str | None = None, email: str | None = None, telephone: str | None = None, address: str | None = None, city: str | None = None ) -> Usuario:
        user = Usuario(
            username=username, 
            password_hash=password_hash, 
            role=role, 
            institution_name=institution_name,
            full_name=full_name,
            document_type=document_type,
            document_number=document_number,
            email=email,
            telephone=telephone,
            address=address,
            city=city
        )
        self.session.add(user)
        self.session.flush()
        return user


    def store_refresh(self, jti: str, user_id: int, seconds: int):
        rt = RefreshToken(
        jti=jti,
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=seconds),
        revoked=False,
        )
        self.session.add(rt)
        self.session.flush() # <-- CORRECCIÓN AÑADIDA


    def get_refresh(self, jti: str) -> Optional[RefreshToken]:
        return self.session.execute(
            select(RefreshToken).where(RefreshToken.jti == jti)
        ).scalar_one_or_none()


    def revoke_refresh(self, jti: str):
        self.session.execute(
            update(RefreshToken).where(RefreshToken.jti == jti).values(revoked=True)
        )

