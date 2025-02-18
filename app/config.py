from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    jwt_secret: str = "none"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 60

    class Config:
        env_prefix = "SECURITY_"

class DjangoSettings(BaseSettings):
    secret_key: str = "none"
    class Config:
        env_prefix = "DJANGO"


class DBSettings(BaseSettings):
    host: str = "db"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    name: str = "postgres"
    engine: str = "django.db.backends.postgresql"

    class Config:
        env_prefix = "DB_"


class SuperuserConfig(BaseSettings):
    username: str = "admin"
    password: str = "admin"
    email: str = "admin@excample.com"


class RedisConfig(BaseSettings):
    host: str = "redis"
    port: int = 6379


class TaskConfig(BaseSettings):
    every: float = 60.0


class Settings(BaseSettings):
    security: SecuritySettings = SecuritySettings()
    db: DBSettings = DBSettings()
    redis: RedisConfig = RedisConfig()
    task: TaskConfig = TaskConfig()
    django: DjangoSettings = DjangoSettings()
    domain: str = "example.com"
    superuser: SuperuserConfig = SuperuserConfig()
    debug: bool = False
    loglevel: str = "INFO"


settings = Settings()
