import os


def must_getenv(key: str) -> str:
    val = os.getenv(key)
    assert val is not None, f"Environment variable of '{key}' is undefined"
    return val
