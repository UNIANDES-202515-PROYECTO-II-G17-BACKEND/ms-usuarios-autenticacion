from typing import List, Optional
from sqlalchemy.orm import Session
from src.repositories.user_repository import UserRepository
from src.domain.models import Usuario

class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repository = UserRepository(session)

    def get_users(self, role: Optional[str] = None, offset: int = 0, limit: int = 100) -> List[Usuario]:
        return self.user_repository.get_users(role, offset=offset, limit=limit)

    def get_user_by_id(self, user_id: int) -> Optional[Usuario]:
        return self.user_repository.get_by_id(user_id)
