import os

from version_utils import modify_item_hidden_attribute, get_version_from_bytes, get_game_folder_version
from src.core.config import Config


class VersionManager:
    def __init__(self):
        self.config_data = Config().config_data

    def switch_version(self, target_version: str):
        etb_installed_path = self.config_data["paths"]["etb_installed_path"]
        current_loaded_version = get_game_folder_version(etb_installed_path)
        z_path = os.path.join(os.path.dirname(etb_installed_path), f"z_ETB{current_loaded_version}")
        os.rename(etb_installed_path,
                  z_path)
        modify_item_hidden_attribute(z_path, True)

        target_version_folder = self.get_target_version_folder(steam_common_folder=os.path.dirname(etb_installed_path),
                                                               target_version=target_version)
        os.rename(target_version_folder, etb_installed_path)
        modify_item_hidden_attribute(etb_installed_path, False)

    @staticmethod
    def get_target_version_folder(steam_common_folder: str, target_version: str) -> str:
        for item in os.listdir(steam_common_folder):
            if item.startswith("z_ETB"):
                full_game_path = os.path.join(steam_common_folder, item)
                if get_game_folder_version(full_game_path).lower() == target_version.lower():
                    return full_game_path
