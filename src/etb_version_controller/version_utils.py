import os
import subprocess

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


def get_version_from_bytes(main_pak_path: str):
    if not os.path.isfile(main_pak_path):
        main_pak_path_parts = main_pak_path.split(os.sep)
        insert_index = len(main_pak_path_parts) - 4
        main_pak_path_parts[insert_index] = "Backrooms"
        main_pak_path_parts[-1] = "Backrooms-WindowsNoEditor.pak"
        main_pak_path = os.sep.join(main_pak_path_parts)
        if not os.path.isfile(main_pak_path):
            return False

    pak_size = os.path.getsize(main_pak_path)

    if pak_size in version_bytes_lookup:
        return version_bytes_lookup[pak_size]
    else:
        return None


def modify_item_hidden_attribute(item_path: str, hidden: bool = True):
    if hidden:
        hidden_command = "+H"
    else:
        hidden_command = "-H"
    item_path = os.path.abspath(item_path)
    subprocess.run(['attrib', hidden_command, item_path], check=True)


def get_game_folder_version(game_folder: str) -> str:
    version_file = os.path.join(game_folder, "version_name.txt")
    with open(version_file, 'r') as file:
        return file.readline().strip()
