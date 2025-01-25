import customtkinter
import os
import shutil

from src.core.config import Config


class UE4SSManager:
    def __init__(self):
        self.config = Config()

        self.local_ue4ss_path = os.path.join(self.config.content_root, r"mod_loaders/ue4ss")
        self.etb_win64_path = os.path.join(self.config.config_data["paths"]["etb_installed_path"],
                                           r"EscapeTheBackrooms\Binaries\Win64")

        self.ue4ss_locally_installed = os.path.isfile(os.path.join(self.local_ue4ss_path, "dwmapi.dll"))

        self.ue4ss_enabled = customtkinter.BooleanVar(
            value=os.path.isfile(os.path.join(self.etb_win64_path, "dwmapi.dll")))

    def update_ue4ss_enabled(self):
        self.ue4ss_enabled.set(os.path.isfile(os.path.join(self.etb_win64_path, "dwmapi.dll")))

    def switch(self):
        ue4ss_active = os.path.isfile(os.path.join(self.etb_win64_path, "dwmapi.dll"))
        switch_enabled = self.ue4ss_enabled.get()
        if ue4ss_active and not switch_enabled:
            if os.path.exists(self.local_ue4ss_path):
                shutil.rmtree(self.local_ue4ss_path)
            os.makedirs(self.local_ue4ss_path, exist_ok=True)

            to_keep = ["Backrooms-Win64-Shipping.exe", "OpenImageDenoise.dll", "tbb12.dll"]
            for filename in os.listdir(self.etb_win64_path):
                if filename not in to_keep:
                    shutil.move(os.path.join(self.etb_win64_path, filename), os.path.join(self.local_ue4ss_path, filename))
        elif not ue4ss_active and switch_enabled:
            if os.path.exists(self.local_ue4ss_path):
                for filename in os.listdir(self.local_ue4ss_path):
                    full_path = os.path.join(self.local_ue4ss_path, filename)
                    if os.path.isdir(full_path):
                        shutil.copytree(full_path, os.path.join(self.etb_win64_path, filename))
                    else:
                        shutil.copy2(full_path, os.path.join(self.etb_win64_path, filename))
