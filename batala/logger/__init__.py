import logging
import logging.config
import os
from pathlib import Path
import yaml

path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

DEFAULT_FILE = Path(dirpath, "default.yaml")


DEFAULT_LOGGER = None
if not DEFAULT_LOGGER:
    with open(DEFAULT_FILE, "r") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)
    DEFAULT_LOGGER = logging.getLogger("engine")
