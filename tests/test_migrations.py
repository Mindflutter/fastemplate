from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import ScriptDirectory


def test_migrations_stairway(alembic_config: Config):
    """Test all revisions.

    Reference: https://github.com/alvassin/backendschool2019/blob/master/tests/migrations/test_stairway.py
    """

    revisions_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    for revision in revisions:
        upgrade(alembic_config, revision.revision)
        # initial revision downgrade uses "-1"
        downgrade(alembic_config, revision.down_revision or "-1")  # type: ignore
        upgrade(alembic_config, revision.revision)

    # downgrade to base (empty db)
    downgrade(alembic_config, "base")
