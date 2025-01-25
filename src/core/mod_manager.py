# Entry point for app - Author [Jedixxx]
import base64

code = base64.b64encode(b"""
from src.ui.ui_manager import UIManager
from src.core.setup import Setup


class ModManagerApp:
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
""")

exec(base64.b64decode(code))
