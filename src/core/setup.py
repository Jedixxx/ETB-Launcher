import os
import sys
import winreg
import vdf
import json
import time

from src.etb_version_controller.version_utils import get_game_version_from_bytes, modify_item_hidden_attribute


class Setup:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            content_root = os.path.dirname(sys.executable)
        else:
            content_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

        self.config_path = os.path.join(content_root, 'config/app_config.json')

        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"SOFTWARE\Valve\Steam")
        self.steam_path, _ = winreg.QueryValueEx(key, "SteamPath")

    def is_config_setup(self) -> bool:
        if os.path.isfile(self.config_path):
            return True
        return False

    def create_version_name_file(self):
        etb_installed_path = self._get_etb_installed_path(self.steam_path)
        game_version = get_game_version_from_bytes(etb_installed_path)
        version_file_path = os.path.join(etb_installed_path, "version_name.txt")
        attempts = 0
        while attempts < 10:
            try:
                with open(version_file_path, 'w') as file:
                    file.write(game_version)
                    break
            except PermissionError:
                if attempts < 10:
                    attempts += 1
                    time.sleep(0.05)
                else:
                    raise

        modify_item_hidden_attribute(version_file_path, True)

    def write_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        steam_exe_path = self._get_steam_exe_path(self.steam_path)
        etb_installed_path = self._get_etb_installed_path(self.steam_path)
        etb_appdata_path = self._get_etb_appdata_path()

        app_config = {"paths": {
            "etb_installed_path": f"{etb_installed_path}",
            "etb_appdata_path": f"{etb_appdata_path}",
            "steam_path": f"{steam_exe_path}"},
            "ui": {
                "dimensions": "1536x864",
                "appearance_mode": "dark",
                "color_theme": "dark-blue"},
            "misc": {
                "refresh_time": 100
            }}
        with open(self.config_path, "w") as f:
            json.dump(app_config, f, indent=4)

    @staticmethod
    def _get_steam_exe_path(steam_path):
        return os.path.join(steam_path, "steam.exe")

    @staticmethod
    def _get_etb_installed_path(steam_path):
        lib_folders = os.path.join(steam_path, r"steamapps/libraryfolders.vdf")
        with open(lib_folders, "r") as f:
            vdf_data = vdf.load(f)
            for universe in vdf_data["libraryfolders"]:
                if vdf_data["libraryfolders"][universe]["apps"].get(None, "1943950"):
                    etb_installed_path = os.path.join(vdf_data["libraryfolders"][universe]["path"],
                                                      r"steamapps\common\EscapeTheBackrooms")
                    if os.path.isfile(os.path.join(etb_installed_path, "Backrooms.exe")):
                        return etb_installed_path

    @staticmethod
    def _get_etb_appdata_path():
        return os.path.join(os.getenv("LOCALAPPDATA"), "EscapeTheBackrooms")
