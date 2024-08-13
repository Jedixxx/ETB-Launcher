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


class ModManagerApp:
    """
    The main application class for the mod manager
    """

    def __init__(self):
        self.ui_manager = UIManager()
        self.ui_manager.load_ui()

    def mainloop(self):
        self.ui_manager.root.mainloop()


if __name__ == "__main__":
    app = ModManagerApp()
    app.mainloop()
