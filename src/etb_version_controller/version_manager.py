import os

from src.etb_version_controller.version_utils import modify_item_hidden_attribute, get_game_folder_version
from src.core.config import Config


class VersionManager:
    def __init__(self):
        self.config_data = Config().config_data

        self.etb_installed_path = self.config_data["paths"]["etb_installed_path"]

    def switch_version(self, target_version: str) -> None:
        """
        Takes a target version and attempts to make this target version the current version of the game
        It does this via renaming files - converts the current directory to a hidden one that can be accessed later
        The target version is searched for and then renamed to the directory that the game accesses

        :param target_version: This a string of the version name e.g "4.5" or "1.21"
        """

        current_loaded_version = get_game_folder_version(self.etb_installed_path)
        if current_loaded_version == target_version:
            return  # No need to switch versions if correct version is already loaded

        z_path = os.path.join(os.path.dirname(self.etb_installed_path), f"z_ETB{current_loaded_version}")
        os.rename(self.etb_installed_path,
                  z_path)
        modify_item_hidden_attribute(z_path, True)

        target_version_folder = self.get_folder_of_target_version(
            steam_common_folder=os.path.dirname(self.etb_installed_path),
            target_version=target_version)
        os.rename(target_version_folder, self.etb_installed_path)
        modify_item_hidden_attribute(self.etb_installed_path, False)

    @staticmethod
    def get_folder_of_target_version(steam_common_folder: str, target_version: str) -> str:
        """
        Takes a target version and searches the steam common folder for game files which match with the target version

        :param steam_common_folder: This is the directory to the Steam/steamapps/common directory
        :param target_version: This a string of the version name e.g "4.5" or "1.21"
        """
        for item in os.listdir(steam_common_folder):
            if item.startswith("z_ETB"):
                full_game_path = os.path.join(steam_common_folder, item)
                if get_game_folder_version(full_game_path).lower() == target_version.lower():
                    return full_game_path

    def get_available_versions(self) -> list[str]:
        steam_common_folder = os.path.dirname(self.etb_installed_path)
        available_versions = []

        # Gets currently loaded version
        current_loaded_version = get_game_folder_version(self.etb_installed_path)
        available_versions.append(current_loaded_version)

        # Gets all versions which are stored in hidden "z" files
        for item in os.listdir(steam_common_folder):
            if item.startswith("z_ETB"):
                full_game_path = os.path.join(steam_common_folder, item)
                available_versions.append(get_game_folder_version(full_game_path).lower())

        return available_versions
