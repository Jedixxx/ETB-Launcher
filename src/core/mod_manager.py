"""
mod_manager.py

This module is the main entry point for the Mod Manager App.

Key Components Explained:
-
-
-

Usage:
Run this script with all required dependencies installed and the config file configured (config/app_config.json)
It opens a window in which u can interact with the app

Author: [Jedixxx]
"""

from src.ui.ui_manager import UIManager
from src.core.setup import Setup


class ModManagerApp:
    """
    The main application class for the mod manager
    """

    def __init__(self):
        self.ui_manager = UIManager()
        self.ui_manager.load_ui()

    def mainloop(self):
        self.ui_manager.update_loop()
        self.ui_manager.root.mainloop()


if __name__ == "__main__":
    setup = Setup()
    if not setup.is_config_setup():
        setup.write_config()
        setup.create_version_name_file()

    app = ModManagerApp()
    app.mainloop()
