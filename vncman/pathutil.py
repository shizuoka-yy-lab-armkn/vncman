import os
from pathlib import Path


def homedir2tilde(path: str, home: str | Path) -> str:
    """
    >>> homedir2tilde("/home/bob/xxx/hello.txt", "/home/bob")
    '~/xxx/hello.txt'
    """
    home = os.path.normpath(home)
    if path.startswith(home):
        return os.path.join("~", path.removeprefix(home + "/"))

    return path
