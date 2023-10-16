# ruff: noqa: T201 (allow print)
import subprocess
from pathlib import Path

import fire

from vncman import osutil
from vncman.config.color import CYAN, GREEN, RESET
from vncman.config.config import DEFAULT_CONFIG_FILE, load_config
from vncman.logger import logger
from vncman.pathutil import homedir2tilde
from vncman.vncserver import VncServerInfo, list_running_servers

HOME = Path(osutil.must_getenv("HOME"))
USER = osutil.must_getenv("USER")


def _print_running_server_infos(servers: list[VncServerInfo]) -> None:
    for s in servers:
        print(
            "  {} (port={}, display=:{}, pid={})".format(
                homedir2tilde(s.pid_file_path, HOME), s.port, s.display_id, s.pid
            )
        )


def cmd_status() -> None:
    """VNCサーバの起動状態や使用ディスプレイ番号等を表示する。"""
    servers = list_running_servers(HOME)
    if len(servers) == 0:
        print(f"{CYAN}Your VNC server is NOT running.{RESET}")
        return

    print(f"{GREEN}Your VNC server is running:{RESET}")
    _print_running_server_infos(servers)


def cmd_up(
    *,
    config: str = DEFAULT_CONFIG_FILE,
    dryrun: bool = False,
) -> None:
    """VNCサーバを起動する。
    既に起動済みの場合は何もしない。
    """
    # 既に起動済みの場合は何もしない
    servers = list_running_servers(HOME)
    if len(servers) > 0:
        print(f"{CYAN}Your VNC server is already running!{RESET}")
        _print_running_server_infos(servers)
        return

    # 設定ファイルを読み込んで実行ユーザに割り当てられたdisplayを取得する
    cfg = load_config(config)
    display_id = cfg.display_mappings.get(USER)
    if display_id is None:
        logger.error(
            "Display ID for user '%s' is not counfigured:\n\tNo entry found in %s",
            USER,
            config,
        )
        exit(1)

    # 起動コマンドを実行
    cmd: list[str] = [
        "vncserver",
        "-depth",
        "24",
        "-geometry",
        "1920x1080",
        f":{display_id}",
    ]
    logger.info(f"Launching: `{' '.join(cmd)}`")
    if dryrun:
        return

    subprocess.run(cmd, check=True)

    # VNCサーバの状態をチェック・表示
    servers = list_running_servers(HOME)
    if len(servers) == 0:
        logger.error("Launched VNC server, but pid file was not wrote.")
        subprocess.run(f"pgrep -u {USER} Xtightvnc | xargs kill", shell=True)
        exit(1)

    print(f"{GREEN}[OK] Successfully launched your VNC server:{RESET}")
    _print_running_server_infos(servers)


def cmd_down() -> None:
    servers = list_running_servers(HOME)
    if len(servers) == 0:
        print(f"{CYAN}Your VNC server is NOT running.{RESET}")
        return

    for s in servers:
        cmd = ["vncserver", "-kill", f":{s.display_id}"]
        logger.info(f"Executing: `{' '.join(cmd)}`")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    fire.Fire(
        name="vncman",
        component={
            "status": cmd_status,
            "up": cmd_up,
            "down": cmd_down,
        },
    )
