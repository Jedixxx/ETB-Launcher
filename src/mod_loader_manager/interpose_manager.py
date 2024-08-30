import customtkinter
import os
import shutil

from src.core.config import Config


class InterposeManager:
    def __init__(self):
        self.config = Config()

        self.etb_mod_folder = os.path.join(self.config.config_data["paths"]["etb_installed_path"],
                                           r"EscapeTheBackrooms\Content\Paks\~mods")

        self.local_interpose_path = os.path.join(self.config.content_root, r"mod_loaders/interpose/Z_Interpose_P.pak")
        self.interpose_game_path = os.path.join(self.etb_mod_folder, "Z_Interpose_P.pak")

        self.interpose_enabled = customtkinter.BooleanVar(value=os.path.isfile(self.interpose_game_path))

    def switch(self):
        if not os.path.isdir(self.etb_mod_folder):
            print("Created ~mods folder")
            os.mkdir(self.etb_mod_folder)

        interpose_active = os.path.isfile(self.interpose_game_path)
        if self.interpose_enabled.get() and not interpose_active:
            shutil.copy2(self.local_interpose_path, self.interpose_game_path)
        elif not self.interpose_enabled.get() and interpose_active:
            os.remove(self.interpose_game_path)
