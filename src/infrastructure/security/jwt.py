import time
import uuid
import jwt
from src.config import settings

# La clave secreta ahora se lee desde la configuración
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

def issue_access_token(user_id: int, username: str, role: str, institution_name: str | None, is_active: bool, full_name: str | None, document_type: str | None, document_number: str | None, email: str | None, telephone: str | None, address: str | None = None, city: str | None = None) -> tuple[str, int]:
    now = int(time.time())
    exp = now + settings.ACCESS_EXPIRES
    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": str(user_id),
        "username": username,
        "iat": now,
        "exp": exp,
        "scope": "user",
        "role": role,
        "is_active": is_active,
        "address": address,
        "city": city,
    }
    if institution_name:
        payload["institution_name"] = institution_name
    if full_name:
        payload["full_name"] = full_name
    if document_type:
        payload["document_type"] = document_type
    if document_number:
        payload["document_number"] = document_number
    if email:
        payload["email"] = email
    if telephone:
        payload["telephone"] = telephone
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, settings.ACCESS_EXPIRES

def issue_refresh_token(user_id: int) -> tuple[str, int, str]:
    now = int(time.time())
    exp = now + settings.REFRESH_EXPIRES
    jti = str(uuid.uuid4())
    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "jti": jti,
        "typ": "refresh",
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, settings.REFRESH_EXPIRES, jti


def decode_token(token: str):
    return jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms=[ALGORITHM], 
        audience=settings.JWT_AUDIENCE,
        leeway=30,
        options={"require": ["exp"]}
    )
