from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.infrastructure.security.jwt import JWKS

# Nota: sin prefix, definimos el path exacto según tu spec.
router = APIRouter(tags=["jwks"])

@router.get("/.well-known/jwks.json", include_in_schema=False)
async def jwks():
    return JSONResponse(content=JWKS)
