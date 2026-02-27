from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastemplate.common.constants import PROJECT_ROOT


class Settings(BaseSettings):
    # read local.env from project root if it exists
    model_config = SettingsConfigDict(env_file=str(PROJECT_ROOT / "local.env"))

    log_level: str = "INFO"
    postgres_dsn: PostgresDsn
