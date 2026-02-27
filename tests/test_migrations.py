import pytest
import sqlalchemy
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import ScriptDirectory

from fastemplate.common.constants import PROJECT_ROOT


@pytest.fixture
def migrations_dsn(postgres_dsn: str) -> str:
    """Create a separate db for migrations testing and return its dsn. Use the same container as postgres_dsn."""
    dsn_prefix = postgres_dsn.rsplit("/", 1)[0]  # dsn base without db name
    admin_dsn = f"{dsn_prefix}/postgres"
    migrations_dsn = f"{dsn_prefix}/test_migrations"

    engine = sqlalchemy.create_engine(admin_dsn, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text('CREATE DATABASE "test_migrations"'))

    return migrations_dsn


def test_migrations_stairway(migrations_dsn: str):
    """Reference:
    https://github.com/alvassin/alembic-quickstart/blob/master/README_ru.md
    https://github.com/alvassin/alembic-quickstart/blob/master/assets/stairway.gif
    """
    # create alembic config, inject test_migrations db connection
    alembic_config = Config(toml_file=PROJECT_ROOT / "pyproject.toml")
    alembic_config.set_main_option("sqlalchemy.url", migrations_dsn)

    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(alembic_config)

    # Get & sort migrations, from first to last
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    for revision in revisions:
        upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)
