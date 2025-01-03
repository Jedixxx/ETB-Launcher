import errno
import os
import shutil
import customtkinter

from src.core.config import Config


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

        self.etb_mod_folder = os.path.join(self.config.config_data["paths"]["etb_installed_path"],
                                           r"EscapeTheBackrooms\Content\Paks\LogicMods")
        self.local_mod_folder = os.path.join(self.config.content_root, "mods")

    def load_local_mods(self):
        """
        Ran on app startup to load all local mods into a "loaded_mods" list.
        """
        for filename in os.listdir(self.local_mod_folder):
            mod_active = os.path.isfile(os.path.join(self.etb_mod_folder, filename))
            self.loaded_mods.append(Mod(filename, mod_active))

    def load_new_mod(self, filepath: str):
        """
        Used during runtime to add a filepath to the local mods folder and to the "loaded_mods" list
        :param filepath: Filepath of the mod
        """
        filename = os.path.basename(filepath)
        shutil.copy2(filepath, os.path.join(self.etb_mod_folder, filename))
        self.loaded_mods.append(Mod(filename, False))

    def update_mod_positions(self):
        # Creates LogicMods folder if needed
        if not os.path.isdir(self.etb_mod_folder):
            print("Created LogicMods folder")
            os.mkdir(self.etb_mod_folder)

        # First reset mods folder
        for filename in os.listdir(self.etb_mod_folder):
            full_path = os.path.join(self.etb_mod_folder, filename)
            if filename.endswith(".pak") and filename != "Z_Interpose_P.pak":
                if filename in os.listdir(self.local_mod_folder):
                    os.remove(full_path)
                else:
                    try:
                        os.rename(full_path, os.path.join(self.local_mod_folder, filename))
                    except OSError as e:
                        if e.errno == errno.EXDEV:
                            shutil.move(full_path, os.path.join(self.local_mod_folder, filename))
                        else:
                            raise

        for mod in self.loaded_mods:
            if mod.activated.get():
                shutil.copy2(os.path.join(self.local_mod_folder, mod.filename),
                             os.path.join(self.etb_mod_folder, mod.filename))

