from pydantic import Field
from environs import Env
from typing import Optional

env = Env()
env.read_env()


class Settings:
    # Database
    db_host: str = env.str("DB_HOST", "localhost")
    db_port: int = env.int("DB_PORT", 5432)
    db_user: str = env.str("DB_USER", "postgres")
    db_password: str = env.str("DB_PASSWORD", "postgres")
    db_name: str = env.str("DB_NAME", "inventory_db")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Redis (для кэширования)
    redis_host: str = env.str("REDIS_HOST", "localhost")
    redis_port: int = env.int("REDIS_PORT", 6379)

    # Server
    debug: bool = env.bool("DEBUG", False)
    host: str = env.str("HOST", "0.0.0.0")
    port: int = env.int("PORT", 8000)


settings = Settings()