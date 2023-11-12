import hashlib
from importlib import util
import os
from pathlib import Path
import sys
from typing import TypeVar

T = TypeVar("T")


def safe_hash(string: str):
    """Returns an MD5 hash that is consistent across interpreter runs."""
    cleaned_str = string.strip().upper()
    return int(hashlib.md5(cleaned_str.encode()).hexdigest(), 16)


def is_module(path: Path) -> bool:
    """Checks if a file path is a module."""
    name = os.path.split(path)[-1]
    if os.path.isfile(path) and name.endswith(".py") and name != "__init__.py":
        return True
    return False


# TODO All this module loading should use standard importlib SourceFileLoader
def load_module(path: Path):
    """Load module from filepath."""
    name = os.path.split(path)[-1]
    module_name = name.strip(".py")
    spec = util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Could not import module from {path}")
    module = util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# TODO All this module loading should use standard importlib SourceFileLoader
def load_path(path: Path):
    """Load modules from path to file/directory."""
    modules = []
    if is_module(path):
        modules.append(path)
    if os.path.isdir(path):
        for file in os.listdir(path):
            module = Path(path, file)
            if is_module(module):
                modules.append(module)
    for module in modules:
        load_module(module)


class Registry(dict[int, T]):
    """Simple registry which wraps a dict with ints for keys.
    Also includes convenience functions for converting strings to int keys.
    """

    def __init__(self, dict: dict | None = None):
        if dict is None:
            dict = {}
        super().__init__({Registry.get_id(key): value for (key, value) in dict.items()})

    @classmethod
    def get_id(cls, key: int | str) -> int:
        """Get a registry id.

        Args:
            key (int | str): the key to convert

        Returns:
            int: an int registry key
        """
        if isinstance(key, int):
            return key
        if isinstance(key, str):
            return safe_hash(key)

    def get_value(self, key: int | str) -> T | None:
        """Get a registry value.

        Args:
            key (int | str): registry key to get value for

        Returns:
            T | None: Registry value if key is registered, else None
        """
        key = self.get_id(key)
        if key not in self:
            return None
        return self[key]

    def __getitem__(self, __key: int | str) -> T:
        return super().__getitem__(self.get_id(__key))

    def __setitem__(self, __key: int | str, val: T):
        super().__setitem__(self.get_id(__key), val)


class BatalaError(Exception):
    def __init__(
        self, message: str = "Unknown BatalaEngine error.", *args: object
    ) -> None:
        self.message = message
        super().__init__(self.message, *args)


class PluginError(BatalaError):
    def __init__(self, plugin, message: str = "", *args: object) -> None:
        self.plugin = plugin
        self.message = message
        super().__init__(self.plugin, self.message, *args)


class APIError(BatalaError):
    def __init__(self, api, message: str = "", *args: object) -> None:
        self.api = api
        self.message = message
        super().__init__(self.api, self.message, *args)
