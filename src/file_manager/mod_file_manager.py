import errno
import os
import shutil
import customtkinter

from src.core.config import Config
from src.etb_version_controller.version_utils import get_game_version_from_bytes


class Mod:
    def __init__(self, filename, activated):
        self.filename = filename
        self.name = self.filename[:-4]  # Removes the .pak file extension
        self.activated = customtkinter.BooleanVar(value=activated)
        self.is_favorite = False


class ModFileManager:
    def __init__(self):
        self.config = Config()
        self.loaded_mods = []

        self.game_path = self.config.config_data["paths"]["etb_installed_path"]

        self.local_mod_folder = os.path.join(self.config.content_root, "mods")

    def _get_mod_folder(self) -> str:
        if get_game_version_from_bytes(self.game_path) == "1.21":
            return os.path.join(self.game_path, r"Backrooms\Content\Paks\LogicMods")
        return os.path.join(self.game_path, r"EscapeTheBackrooms\Content\Paks\LogicMods")

    def load_local_mods(self):
        """
        Ran on app startup or runtime to load all local mods into a "loaded_mods" list.
        """
        self.loaded_mods.clear()
        for filename in os.listdir(self.local_mod_folder):
            mod_active = os.path.isfile(os.path.join(self._get_mod_folder(), filename))
            self.loaded_mods.append(Mod(filename, mod_active))

    def update_mod_positions(self):
        etb_mod_folder = self._get_mod_folder()
        # Creates LogicMods folder if needed
        if not os.path.isdir(etb_mod_folder):
            os.mkdir(etb_mod_folder)
            print("Created LogicMods folder")

        # First reset Paks folder
        self._explore_and_filter_dir(os.path.dirname(etb_mod_folder))

        for mod in self.loaded_mods:
            if mod.activated.get():
                shutil.copy2(os.path.join(self.local_mod_folder, mod.filename),
                             os.path.join(etb_mod_folder, mod.filename))

    def _explore_and_filter_dir(self, directory: str):
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                self._explore_and_filter_dir(entry_path)
                if not os.listdir(entry_path) and entry != "LogicMods":
                    os.rmdir(entry_path)
            elif os.path.isfile(entry_path):
                if (entry.endswith(".pak") and not entry_path.endswith(os.path.join("LogicMods", "Z_Interpose_P.pak"))
                        and entry not in ["Backrooms-WindowsNoEditor.pak", "EscapeTheBackrooms-WindowsNoEditor.pak"]):
                    if entry in os.listdir(self.local_mod_folder):
                        os.remove(entry_path)
                    else:
                        try:
                            os.rename(entry_path, os.path.join(self.local_mod_folder, entry))
                        except OSError as e:
                            if e.errno == errno.EXDEV:
                                shutil.move(entry_path, os.path.join(self.local_mod_folder, entry))
                            else:
                                raise
