import customtkinter
import os
import shutil

from src.core.config import Config


class UE4SSManager:
    def __init__(self):
        self.config = Config()

        self.etb_win64_path = os.path.join(self.config.config_data["paths"]["etb_installed_path"],
                                           r"EscapeTheBackrooms\Binaries\Win64")

        self.ue4ss_enabled = customtkinter.BooleanVar(value=os.path.isfile(self.interpose_game_path))
