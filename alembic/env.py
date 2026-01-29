from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.infrastructure.database.models import Base
from app.core.config import settings

# Настройка логгера
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔑 Ключевое: подставляем URL из настроек
config.set_main_option("sqlalchemy.url", settings.database_url)

# Метаданные для автогенерации
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()