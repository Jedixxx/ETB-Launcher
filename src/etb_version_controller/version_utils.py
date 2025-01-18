import os
import subprocess
from typing import Optional

# A lookup which matches bytes of the WindowsNoEditor.pak file with the equivalent version
version_bytes_lookup = {
    23484460097: "4.5",
    23484470337: "4.4",
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


def modify_item_hidden_attribute(item_path: str, hidden: bool = True):
    if hidden:
        hidden_command = "+H"
    else:
        hidden_command = "-H"
    item_path = os.path.abspath(item_path)
    subprocess.run(['attrib', hidden_command, item_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)


def get_game_folder_version(game_folder: str) -> str:
    version_file = os.path.join(game_folder, "version_name.txt")

    with open(version_file, 'r') as file:
        return file.readline().strip()


def are_files_accessible(files: list[str]):
    for filepath in files:
        try:
            with open(filepath, 'r'):
                pass
        except (PermissionError, FileNotFoundError) as e:
            print(e)
            return False
    return True


def get_game_version_from_bytes(game_folder: str) -> Optional[str]:
    """
    Using the version byte lookup retrieves the version of a game version using the WindowsNoEditor.pak file
    Checks both the update 1 and post update 1 paths for the pak file

    :param game_folder: The root folder of the game version
    :return: A string representing the match version if is found, otherwise None
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

    return None
