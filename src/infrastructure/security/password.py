from passlib.context import CryptContext
import bcrypt


if not hasattr(bcrypt, "__about__"):
    import types
    bcrypt.__about__ = types.SimpleNamespace(__version__=bcrypt.__version__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)