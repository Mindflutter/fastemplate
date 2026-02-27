import sqlalchemy as sa
from sqlalchemy import MetaData, func

metadata = MetaData()

example_tbl = sa.Table(
    "example",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(length=30), unique=True),
    sa.Column("description", sa.String(length=1024), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
