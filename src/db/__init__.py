from sqlalchemy.orm import declarative_base

Base = declarative_base()

# models must be imported after declarative base init
# pylint: disable=wrong-import-position
from db.example import Example
