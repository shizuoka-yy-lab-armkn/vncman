import tomllib

from pydantic import BaseModel

from vncman.logger import logger

Username = str
DisplayId = int


class Config(BaseModel):
    display_mappings: dict[Username, DisplayId]


DEFAULT_CONFIG_FILE = "/etc/vncman/config.toml"


def load_config(path: str = DEFAULT_CONFIG_FILE) -> Config:
    logger.info("Loading configuration from '%s'", path)
    with open(path, "rb") as f:
        obj = tomllib.load(f)
        return Config(**obj)
