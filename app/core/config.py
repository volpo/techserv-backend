from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TechServ API"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://techserv:techserv@localhost:5432/techserv"
    database_url_sync: str = "postgresql://techserv:techserv@localhost:5432/techserv"

    supabase_url: str = ""
    supabase_jwt_secret: str = "dev-secret-change-in-production"

    redis_url: str = "redis://localhost:6379/0"

    cors_origins: str = "http://localhost:3000,http://localhost:8081"

    jwt_algorithm: str = "HS256"
    testing: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
