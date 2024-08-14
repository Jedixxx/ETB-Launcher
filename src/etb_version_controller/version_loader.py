import os
import shutil

from version_utils import modify_item_hidden_attribute, get_game_folder_version, get_version_from_bytes
from src.core.config import Config


class VersionLoader:
    def __init__(self):
        self.config_data = Config().config_data
        self.decentralised_versions = []

    def centralise_versions(self):
        for game_folder in self.decentralised_versions:
            print("Centralising Versions... (This may take a long time)")

            game_version = get_game_folder_version(game_folder)
            etb_installed_path = self.config_data["paths"]["etb_installed_path"]

            z_path = os.path.join(os.path.dirname(etb_installed_path), f"z_ETB{game_version}")
            os.rename(game_folder,
                      z_path)
            modify_item_hidden_attribute(z_path, True)

    def load_local_version(self, game_folder: str, game_folder_version: str):
        version_file_path = os.path.join(game_folder, "version_name.txt")
        if os.path.isfile(version_file_path):
            os.remove(version_file_path)
        with open(version_file_path, 'w') as file:
            file.write(game_folder_version)
        modify_item_hidden_attribute(version_file_path, True)

        self.decentralised_versions.append(game_folder)

    @staticmethod
    def get_game_version_from_bytes(game_folder: str):
        return get_version_from_bytes(os.path.join(game_folder, r"EscapeTheBackrooms\Content\Paks\EscapeTheBackrooms-WindowsNoEditor.pak"))
