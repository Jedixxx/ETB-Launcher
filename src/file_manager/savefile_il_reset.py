import os
import shutil
from pynput import keyboard
from src.core.config import Config


class SaveFileReset:
    def __init__(self):
        appdata_path = Config().config_data["paths"]["etb_appdata_path"]
        self.savegames_path = os.path.join(appdata_path, r"Saved\SaveGames")
        self.target = None
        self.keybind = None
        self.listener = keyboard.Listener(on_press=self._copy_file_in)

    def _copy_file_in(self, key):
        if str(key) == self.keybind:
            dst = os.path.join(self.savegames_path, os.path.basename(self.target))
            if os.path.exists(dst):
                os.remove(dst)
            if self.target != dst:
                shutil.copy2(self.target, dst)

    def start_listen(self, target):
        self.target = target
        if not os.path.exists(target) or os.path.basename(target)[-4:] != ".sav":
            return None
        print("Listening...")
        self.listener.start()

    def stop_listen(self):
        self.target = None
        print("Stopped Listening...")
        self.listener.stop()
        self.listener = keyboard.Listener(on_press=self._copy_file_in) # Remake thread

    def set_keybind(self):
        def on_first_press(key):
            listener.stop()
            self.keybind = str(key)
            print(f"Keybind set to {self.keybind}")
            return key

        with keyboard.Listener(on_press=on_first_press) as listener:
            listener.join()
