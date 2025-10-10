from src.repositories.user_repository import UserRepository
from src.infrastructure.security.password import verify_password, hash_password
from src.infrastructure.security import jwt as jwtsec


class AuthService:

    def __init__(self, session):
        self.repo = UserRepository(session)
        self.session = session


    def register_if_absent(self, username: str, password: str, role: str, institution_name: str):
        if self.repo.get_by_username(username):
            return None, "Usuario ya existe"
        user = self.repo.create_user(
            username=username,
            password_hash=hash_password(password),
            role=role,
            institution_name=institution_name,
        )
        return user, None

    def login(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user or not user.is_active:
            return None, "Credenciales inválidas"
        if not verify_password(password, user.password_hash):
            return None, "Credenciales inválidas"

        access, access_secs, _ = jwtsec.issue_access_token(
            user_id=user.id, 
            username=user.username, 
            role=user.role, 
            institution_name=user.institution_name
        )
        refresh, refresh_secs, jti_refresh = jwtsec.issue_refresh_token(user.id)
        self.repo.store_refresh(jti_refresh, user.id, refresh_secs)

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "expires_in": access_secs,
        }, None


    def refresh(self, refresh_token: str):
        try:
            data = jwtsec.decode_token(refresh_token)
        except Exception:
            return None, "Refresh inválido"

        if data.get("typ") != "refresh":
            return None, "Refresh inválido"


        jti = data.get("jti")
        rt = self.repo.get_refresh(jti)
        if not rt or rt.revoked:
            return None, "Refresh revocado o inexistente"

        user_id = int(data["sub"]) if data.get("sub") else None
        if not user_id:
            return None, "Usuario inválido"

        user = self.repo.get_by_id(user_id)
        if not user:
            return None, "Usuario inválido"

        access, access_secs, _ = jwtsec.issue_access_token(
            user_id=user.id, 
            username=user.username, 
            role=user.role, 
            institution_name=user.institution_name
        )
        return {
            "access_token": access,
            "token_type": "Bearer",
            "expires_in": access_secs,
        }, None