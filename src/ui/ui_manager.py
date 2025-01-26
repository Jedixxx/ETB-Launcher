import customtkinter
from src.ui.components import launch_game, version_switcher, version_adder, mod_list, mod_loader_switches, quick_reset
from src.core.config import Config


class UIManager:
    """
    Handles all UI Presentation and Management
    """

    def __init__(self):
        self.config = Config()

        customtkinter.set_appearance_mode(self.config.config_data["ui"]["appearance_mode"])
        customtkinter.set_default_color_theme(self.config.config_data["ui"]["color_theme"])

        # Overall setup
        self.root = customtkinter.CTk()
        self.root.geometry(self.config.config_data["ui"]["dimensions"])
        self.root.title("Jedixxx's Mod Manager v0.5")
        self.root.resizable(False, False)
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.updating_objects = []
        self.refresh_time = self.config.config_data["misc"]["refresh_time"]

        # Components Setup

        customtkinter.CTkLabel(master=self.frame, text="Jedixxx's Mod Manager",
                               font=("Arial", 30, "bold")).pack(pady=12, padx=10)

        self.mod_loader_switches_controller = mod_loader_switches.ModLoaderSwitches(ui_manager=self, x=708, y=660,
                                                                                    width=250, height=150)

        self.mod_list_controller = mod_list.ModList(ui_manager=self, scrollable_width=600, scrollable_height=700,
                                                    scrollable_x=50, scrollable_y=100)
        self.updating_objects.append(self.mod_list_controller)

        self.launch_button_controller = launch_game.LaunchGame(ui_manager=self, width=400, height=150, x=1000, y=660,
                                                               text_size=40)
        self.updating_objects.append(self.launch_button_controller)

        self.mod_loader_switches_controller = mod_loader_switches.ModLoaderSwitches(ui_manager=self, x=708, y=660,
                                                                                    width=250, height=150)

        self.version_switcher_controller = version_switcher.VersionSwitcher(ui_manager=self, width=340, height=50,
                                                                            x=1060,
                                                                            y=600)
        self.updating_objects.append(self.version_switcher_controller)

        self.version_adder_controller = version_adder.VersionAdder(ui_manager=self, width=50, height=50, x=1000,
                                                                   y=600,
                                                                   root=self.root)

        self.quick_reset_controller = quick_reset.QuickResetUI(ui_manager=self, x=1000, y=70,
                                                               width=400, height=200)
        self.updating_objects.append(self.quick_reset_controller)

    def update_loop(self):
        for object_to_update in self.updating_objects:
            object_to_update.update_function()
        self.root.after(self.refresh_time, self.update_loop)

    def load_ui(self):
        self.mod_list_controller.load()
        self.version_adder_controller.load()
        self.launch_button_controller.load()
        self.version_switcher_controller.load()
        self.mod_loader_switches_controller.load()
        self.quick_reset_controller.load()
