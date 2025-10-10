import os
from datetime import timedelta


class Settings:

    SERVICE_NAME = os.getenv("SERVICE_NAME", "ms-usuarios-autenticacion")
    VERSION = os.getenv("VERSION", "0.1.0")

    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    DB_NAME = os.getenv("POSTGRES_DB", "db_ms_usuarios_aut")


    SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


    DEFAULT_SCHEMA = os.getenv("DEFAULT_SCHEMA", "co")
    COUNTRY_HEADER = os.getenv("COUNTRY_HEADER", "X-Country")


    # JWT
    JWT_ISSUER = os.getenv("JWT_ISSUER", "ms-usuarios-autenticacion")
    ACCESS_EXPIRES = int(os.getenv("ACCESS_EXPIRES", "3600"))
    REFRESH_EXPIRES = int(os.getenv("REFRESH_EXPIRES", "1209600"))

    PRIVATE_KEY_PEM = os.getenv("JWT_PRIVATE_KEY_PEM")
    PUBLIC_KEY_PEM = os.getenv("JWT_PUBLIC_KEY_PEM")
    KEY_ID = os.getenv("JWT_KEY_ID", "kid-1")

settings = Settings()
