from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

class MeResponse(BaseModel):
    id: str
    username: str
    role: str | None = None
    institution_name: str | None = None
    is_active: bool | None = None
    scope: str | None = None
    iss: str | None = None
    aud: str | None = None
    iat: int | None = None
    exp: int | None = None
    full_name: str | None = None
    document_type: str | None = None
    document_number: str | None = None
    email: str | None = None
    telephone: str | None = None

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    institution_name: str | None = None
    full_name: str | None = None
    document_type: str | None = None
    document_number: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None

class RegisterResponse(BaseModel):
    id: int
    username: str
    created_at: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    institution_name: Optional[str] = None
    full_name: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
