import os
from typing import Optional

from src.etb_version_controller.version_utils import modify_item_hidden_attribute, get_game_folder_version
from src.core.config import Config

# A lookup which matches bytes of the WindowsNoEditor.pak file with the equivalent version
version_bytes_lookup = {
    23484460097: "4.5",
    23484477440: "4.0",
    23484474433: "4.0-r",
    17542794007: "3.13",
    17333555436: "3.2",
    17333522772: "3.0",
    9539746925: "2.12",
    9566900394: "2.9",
    9565303893: "2.3",
    4310942093: "1.21"
}


class VersionLoader:
    def __init__(self):
        self.config_data = Config().config_data
        self.etb_installed_path = self.config_data["paths"]["etb_installed_path"]

    def load_local_version(self, game_folder: str, game_folder_version: str):
        version_file_path = os.path.join(game_folder, "version_name.txt")
        if os.path.isfile(version_file_path):
            os.remove(version_file_path)
        with open(version_file_path, 'w') as file:
            file.write(game_folder_version)
        modify_item_hidden_attribute(version_file_path, True)

        self._centralise_version(game_folder)

    def _centralise_version(self, game_folder: str):
        print("Centralising Version... (This may take a long time)")
        game_version = get_game_folder_version(game_folder)
        z_path = os.path.join(os.path.dirname(self.etb_installed_path), f"z_ETB{game_version}")
        os.rename(game_folder,
                  z_path)
        modify_item_hidden_attribute(z_path, True)

    @staticmethod
    def get_game_version_from_bytes(game_folder: str) -> Optional[str]:
        """
        Using the version byte lookup retrieves the version of a game version using the WindowsNoEditor.pak file
        Checks both the update 1 and post update 1 paths for the pak file

        :param game_folder: The root folder of the game version
        :return: A string representing the match version if is found, otherwise None
        :raises FileNotFoundError: If neither potential .pak file paths are not found
        """

        potential_paths = [
            # Post Update 1 path
            os.path.join(game_folder, r"EscapeTheBackrooms\Content\Paks\EscapeTheBackrooms-WindowsNoEditor.pak"),
            # Update 1 path
            os.path.join(game_folder, r"Backrooms\Content\Paks\Backrooms-WindowsNoEditor.pak")
        ]

        for potential_path in potential_paths:
            if os.path.isfile(potential_path):
                pak_size = os.path.getsize(potential_path)
                return version_bytes_lookup.get(pak_size, None)

        raise FileNotFoundError(f"Cannot locate .pak file from any expected paths: {potential_paths}")
