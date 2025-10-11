import os
from datetime import timedelta


class Settings:

    SERVICE_NAME = os.getenv("SERVICE_NAME", "ms-usuarios-autenticacion")
    VERSION = os.getenv("VERSION", "0.1.0")
    REGION = os.getenv("REGION", "us-central1")

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASS", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "db_ms_usuarios_aut")

    REDIS_HOST = os.getenv("REDIS_HOST", "")
    REDIS_PORT = os.getenv("REDIS_PORT", "")

    SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    DEFAULT_SCHEMA = os.getenv("DEFAULT_SCHEMA", "co")
    COUNTRY_HEADER = os.getenv("COUNTRY_HEADER", "X-Country")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-for-local-dev")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "ms-usuarios-autenticacion")
    ACCESS_EXPIRES = int(os.getenv("ACCESS_EXPIRES", "3600"))
    REFRESH_EXPIRES = int(os.getenv("REFRESH_EXPIRES", "1209600"))
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "medisupply-api")

settings = Settings()
