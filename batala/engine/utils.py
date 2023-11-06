import hashlib


def safe_hash(string: str):
    cleaned_str = string.strip().upper()
    return int(hashlib.md5(cleaned_str.encode()).hexdigest(), 16)


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
