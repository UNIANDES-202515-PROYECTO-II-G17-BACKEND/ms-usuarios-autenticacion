import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.domain.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, RegisterRequest, RegisterResponse
from src.services.auth_service import AuthService
from src.dependencies import get_session

router = APIRouter(prefix="/v1/auth", tags=["auth"])

log = logging.getLogger(__name__)

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, session: Session = Depends(get_session)):
    svc = AuthService(session)
    tokens, err = svc.login(payload.username, payload.password)
    if err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err)
    return tokens

@router.post("/refresh", response_model=RefreshResponse)
async def refresh(payload: RefreshRequest, session: Session = Depends(get_session)):
    svc = AuthService(session)
    new_tokens, err = svc.refresh(payload.refresh_token)
    if err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err)
    return new_tokens

@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(payload: RegisterRequest, session: Session = Depends(get_session)):
    svc = AuthService(session)

    user, err = svc.register_if_absent(
        username=payload.username,
        password=payload.password,
        role=payload.role,
        institution_name=payload.institution_name,
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=err)

    return RegisterResponse(
        id=user.id,
        username=user.username,
        created_at=user.created_at.isoformat(),
    )