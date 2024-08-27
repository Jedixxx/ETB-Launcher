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
                                           r"EscapeTheBackrooms\Content\Paks\~mods")
        self.local_mod_folder = os.path.join(self.config.content_root, "mods")

    def load_local_mods(self):
        for filename in os.listdir(self.local_mod_folder):
            mod_active = os.path.isfile(os.path.join(self.etb_mod_folder, filename))
            mod_to_add = Mod(filename, mod_active)
            self.loaded_mods.append(mod_to_add)

    def load_new_mod(self, filepath):
        filename = os.path.basename(filepath)
        mod_to_add = Mod(filename, False)
        self.loaded_mods.append(mod_to_add)

    def update_mod_positions(self):
        # Creates ~mods folder if needed
        if not os.path.isdir(self.etb_mod_folder):
            print("Created ~mods folder")
            os.mkdir(self.etb_mod_folder)

        for mod in self.loaded_mods:
            mod_active = os.path.isfile(os.path.join(self.etb_mod_folder, mod.filename))
            if mod.activated.get() and not mod_active:
                shutil.copy2(os.path.join(self.local_mod_folder, mod.filename),
                             os.path.join(self.etb_mod_folder, mod.filename))
            elif not mod.activated.get() and mod_active:
                os.remove(os.path.join(self.etb_mod_folder, mod.filename))
