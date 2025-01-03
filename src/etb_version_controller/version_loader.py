import os

from src.etb_version_controller.version_utils import modify_item_hidden_attribute, get_game_folder_version
from src.core.config import Config


class VersionLoader:
    """
    A class that handles the logic of loading local versions into a state that can be easily used by the application
    """

    def __init__(self):
        self.config_data = Config().config_data
        self.etb_installed_path = self.config_data["paths"]["etb_installed_path"]

    def load_local_version(self, game_folder: str, game_folder_version: str) -> None:
        """
        Wrapper for the _centralise_version function which creates a version_name.txt in the game version root folder

        :param game_folder: Path to root folder of game version.
        :param game_folder_version: Version of the game folder
        """
        version_file_path = os.path.join(game_folder, "version_name.txt")
        if os.path.isfile(version_file_path):
            os.remove(version_file_path)
        with open(version_file_path, 'w') as file:
            file.write(game_folder_version)
        modify_item_hidden_attribute(version_file_path, True)

        self._centralise_version(game_folder)

    def _centralise_version(self, game_folder: str) -> None:
        """
        Moves a game version folder to the same place ETB is installed
        It makes the folder hidden and start with z, hence "z_path", in order to not disrupt normal user navigation
        :param game_folder: Path to root folder of game version
        """
        game_version = get_game_folder_version(game_folder)
        z_path = os.path.join(os.path.dirname(self.etb_installed_path), f"z_ETB{game_version}")
        os.rename(game_folder,
                  z_path)
        modify_item_hidden_attribute(z_path, True)
