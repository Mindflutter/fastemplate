from fastemplate.repositories.engine import Engine


class BaseRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
