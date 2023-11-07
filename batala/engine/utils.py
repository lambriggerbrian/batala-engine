import hashlib
from typing import Generic, TypeVar

T = TypeVar("T")


def safe_hash(string: str):
    cleaned_str = string.strip().upper()
    return int(hashlib.md5(cleaned_str.encode()).hexdigest(), 16)


class Registry(dict[int, T]):
    def __init__(self, dict: dict | None = None):
        if dict is None:
            dict = {}
        super().__init__({Registry.get_id(key): value for (key, value) in dict.items()})

    @classmethod
    def get_id(cls, key: int | str) -> int:
        if isinstance(key, int):
            return key
        if isinstance(key, str):
            return safe_hash(key)

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
