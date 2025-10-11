import time
import uuid

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from src.config import settings


if settings.PRIVATE_KEY_PEM and settings.PUBLIC_KEY_PEM:
    private_key = serialization.load_pem_private_key(settings.PRIVATE_KEY_PEM.encode(), password=None)
    public_key = serialization.load_pem_public_key(settings.PUBLIC_KEY_PEM.encode())
else:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()


PRIVATE_PEM = private_key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption(),)
PUBLIC_PEM = public_key.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)

def _public_numbers_to_jwk(pubkey, kid: str):
    nums = pubkey.public_numbers()
    e = nums.e.to_bytes((nums.e.bit_length() + 7)//8, 'big')
    n = nums.n.to_bytes((nums.n.bit_length() + 7)//8, 'big')
    from base64 import urlsafe_b64encode

    def b64u(b):
        return urlsafe_b64encode(b).rstrip(b'=').decode('ascii')

    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": "RS256",
        "n": b64u(n),
        "e": b64u(e),
    }

JWKS = {"keys": [_public_numbers_to_jwk(public_key, settings.KEY_ID)]}

def issue_access_token(user_id: int, username: str, role: str, institution_name: str | None) -> tuple[str, int]:
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
    }
    if institution_name:
        payload["institution_name"] = institution_name
    token = jwt.encode(payload, PRIVATE_PEM, algorithm="RS256", headers={"kid": settings.KEY_ID})
    return token, settings.ACCESS_EXPIRES


def issue_refresh_token(user_id: int) -> tuple[str, int, str]:
    now = int(time.time())
    exp = now + settings.REFRESH_EXPIRES
    jti = str(uuid.uuid4())
    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "jti": jti,
        "typ": "refresh",
    }
    token = jwt.encode(payload, PRIVATE_PEM, algorithm="RS256", headers={"kid": settings.KEY_ID})
    return token, settings.REFRESH_EXPIRES, jti

def decode_token(token: str):
    return jwt.decode(
        token, 
        PUBLIC_PEM, 
        algorithms=["RS256"], 
        audience=settings.JWT_AUDIENCE, # <-- Validación de Audience añadida
        options={"require": ["exp", "iat"]}
    )
