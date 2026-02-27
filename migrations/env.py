from alembic import context
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, make_url, pool

from fastemplate.common.constants import PROJECT_ROOT
from fastemplate.repositories.tables import metadata

config = context.config


class MigrationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(PROJECT_ROOT / "local.env"), extra="ignore")

    postgres_dsn: PostgresDsn


# get a db connection url from existing config option or from env vars
POSTGRES_DSN = config.get_main_option("sqlalchemy.url") or make_url(str(MigrationSettings().postgres_dsn)).set(
    drivername="postgresql+psycopg"
)

target_metadata = metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=POSTGRES_DSN,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(POSTGRES_DSN, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
