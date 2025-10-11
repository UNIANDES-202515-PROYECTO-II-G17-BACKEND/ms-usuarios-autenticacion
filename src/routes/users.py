from fastapi import APIRouter, HTTPException, Request, status
from src.domain.schemas import MeResponse
from src.infrastructure.security.jwt import decode_token

router = APIRouter(prefix="/v1/usuarios", tags=["usuarios"])

@router.get("/me", response_model=MeResponse)
async def me(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta token")
    token = auth.split(" ", 1)[1]
    try:
        data = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return {
        "id": data.get("sub"),
        "username": data.get("username"),
        "scope": data.get("scope"),
        "iss": data.get("iss"),
        "role": data.get("role"),
        "institution_name": data.get("institution_name"),
        "aud": data.get("aud"),
        "iat": data.get("iat"),
        "exp": data.get("exp"),
    }
