from pydantic import BaseModel, EmailStr, Field


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

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    institution_name: str | None = None

class RegisterResponse(BaseModel):
    id: int
    username: str
    created_at: str