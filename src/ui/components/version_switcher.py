import time

import customtkinter

from src.etb_version_controller.version_manager import VersionManager


class VersionSwitcher:
    def __init__(self, master, width, height, x, y, launch_button_controller):
        self.version_manager = VersionManager()
        self.launch_button_controller = launch_button_controller
        self.available_versions = self.version_manager.get_available_versions()

        self.version_option_menu = customtkinter.CTkOptionMenu(master=master, width=width, height=height, values=self._format_version_list(self.available_versions), command=self.switch_version)
        self.version_option_menu.place(x=x, y=y)

        self.update_function = self.update_available_versions

    def update_available_versions(self):
        previous_available_version = self.available_versions
        self.available_versions = self.version_manager.get_available_versions()
        if self.available_versions != previous_available_version:
            self.version_option_menu.configure(values=self._format_version_list(self.available_versions))

    def switch_version(self, formatted_target_version):
        if self.launch_button_controller.game_running():
            self.version_option_menu.set("Please close the game before switching version")

        target_version = formatted_target_version.replace("Version ", "")
        self.version_manager.switch_version(target_version=target_version)

    @staticmethod
    def _format_version_list(version_list: list[str]) -> list[str]:
        current_version = version_list[0] # Isolates selected version so it can stay at top
        sorted_version_list = [current_version] + sorted(version_list[1:], reverse=True)

        formatted_version_list = ["Version " + version_number for version_number in sorted_version_list]
        return formatted_version_list

