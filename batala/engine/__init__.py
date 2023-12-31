import logging
import os
from pathlib import Path
from numpy import uint32, left_shift, uint8
from batala import PACKAGE_PATH
from batala.logger import DEFAULT_LOGGER

INDEX_BITS = 24
GENERATION_BITS = 8
INDEX_MASK = left_shift(uint32(1), INDEX_BITS) - 1
GENERATION_MASK = left_shift(uint32(1), GENERATION_BITS) - 1
MAX_ENTITY_VALUE = 2**INDEX_BITS
MAX_ENTITIES = MAX_ENTITY_VALUE - 1
MAX_GENERATION_VALUE = 2**GENERATION_BITS
MAX_GENERATIONS = MAX_GENERATION_VALUE - 1
MINIMUM_FREE_INDICES = 1024

Id = uint32
Index = uint32
Generation = uint8

logger = DEFAULT_LOGGER or logging.getLogger("batala.engine")

path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

DEFAULT_SEARCH_PATHS = [Path(PACKAGE_PATH, "components"), Path(PACKAGE_PATH, "systems")]
