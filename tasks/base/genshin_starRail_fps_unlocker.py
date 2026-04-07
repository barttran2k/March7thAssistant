from module.config import cfg
from module.logger import log
import sys
import os
import hashlib
from utils.console import pause_on_error, pause_and_retry


class Genshin_StarRail_fps_unlocker:
    @staticmethod
    def update():
        from module.update.update_handler import UpdateHandler
        from tasks.base.fastest_mirror import FastestMirror
        import requests
        import json
        response = requests.get(FastestMirror.get_github_api_mirror("winTEuser", "Genshin_StarRail_fps_unlocker"), timeout=10, headers=cfg.useragent)
        if response.status_code == 200:
            data = json.loads(response.text)
            url = None
            expected_size = None
            for asset in data["assets"]:
                if asset["name"].startswith("Unlocker") and asset["name"].endswith(".exe"):
                    url = FastestMirror.get_github_mirror(asset["browser_download_url"])
                    expected_size = asset["size"]
                    break
            if url is None:
                log.error("没有找到可用更新，请稍后再试")
                pause_on_error()
                sys.exit(0)
            update_handler = UpdateHandler(url, cfg.genshin_starRail_fps_unlocker_path, "Genshin_StarRail_fps_unlocker")
            update_handler.download_file_path = os.path.join(cfg.genshin_starRail_fps_unlocker_path, "unlocker.exe")
            update_handler.download_file()
            download_path = update_handler.download_file_path
            if os.path.exists(download_path):
                actual_size = os.path.getsize(download_path)
                if expected_size is not None and actual_size != expected_size:
                    log.error(f"下载文件大小不匹配，文件可能已损坏: 期望 {expected_size} 字节, 实际 {actual_size} 字节")
                    os.remove(download_path)
                    pause_on_error()
                    sys.exit(0)
                with open(download_path, "rb") as f:
                    file_data = f.read()
                if file_data[:2] != b"MZ":
                    log.error("下载文件不是有效的可执行文件")
                    os.remove(download_path)
                    pause_on_error()
                    sys.exit(0)
                sha256_hash = hashlib.sha256(file_data).hexdigest()
                log.info(f"下载文件 SHA256: {sha256_hash}")
        else:
            log.error(f"获取更新信息失败：{response.status_code}")
