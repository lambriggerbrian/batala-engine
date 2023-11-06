import hashlib


def safe_hash(string: str):
    cleaned_str = string.strip().upper()
    return int(hashlib.md5(cleaned_str.encode()).hexdigest(), 16)
