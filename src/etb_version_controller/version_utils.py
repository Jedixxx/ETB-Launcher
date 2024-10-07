import os
import subprocess


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
