import os
from glob import glob
from pathlib import Path
from typing import NamedTuple


class VncServerInfo(NamedTuple):
    display_id: int
    pid: int
    pid_file_path: str

    @property
    def port(self) -> int:
        return 5900 + self.display_id


def list_running_servers(user_home_dir: Path) -> list[VncServerInfo]:
    pid_file_paths = glob(str(user_home_dir / ".vnc" / "*.pid"))

    server_infos: list[VncServerInfo] = []

    for path in pid_file_paths:
        # ファイル名は `{hostname}:{pid}.pid` の形式であることを想定する
        stem, ext = os.path.splitext(os.path.basename(path))
        assert ext == ".pid"
        display_id = int(stem.split(":")[1])

        with open(path) as f:
            pid = int(f.read())

        server_infos.append(
            VncServerInfo(
                display_id=display_id,
                pid=pid,
                pid_file_path=path,
            )
        )

    return server_infos
