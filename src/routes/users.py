import logging
import jwt # Importar la librería jwt para capturar sus excepciones
from fastapi import APIRouter, HTTPException, Request, status
from src.domain.schemas import MeResponse
from src.infrastructure.security.jwt import decode_token

router = APIRouter(prefix="/v1/usuarios", tags=["usuarios"])
log = logging.getLogger(__name__) # Configurar el logger

@router.get("/me", response_model=MeResponse)
async def me(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta token")
    
    token = auth.split(" ", 1)[1]
    try:
        data = decode_token(token)
    except jwt.PyJWTError as e:
        log.error(f"Error de validación de JWT: {e.__class__.__name__} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    data['id'] = data.get('sub')

    return data
