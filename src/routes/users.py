import logging
from typing import List, Optional
import jwt # Importar la librería jwt para capturar sus excepciones
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from src.domain.schemas import MeResponse, UserResponse
from src.infrastructure.security.jwt import decode_token
from src.services.user_service import UserService
from src.dependencies import get_session

router = APIRouter(prefix="/v1/usuarios", tags=["usuarios"])
log = logging.getLogger(__name__) # Configurar el logger

ALLOWED_ROLES = {"admin", "institutional_customer", "seller"}

@router.get("/", response_model=List[UserResponse])
def get_users(role: Optional[str] = None, session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    if role and role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol '{role}' no es válido. Los roles permitidos son: {', '.join(ALLOWED_ROLES)}"
        )
    svc = UserService(session)
    return svc.get_users(role, offset=offset, limit=limit)

@router.get("/usuario/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    svc = UserService(session)
    user = svc.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

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
