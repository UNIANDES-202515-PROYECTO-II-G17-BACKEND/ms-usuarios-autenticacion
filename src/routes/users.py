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
    
    # Mapear el campo 'sub' del token al campo 'id' de la respuesta
    data['id'] = data.get('sub')
    
    return data
