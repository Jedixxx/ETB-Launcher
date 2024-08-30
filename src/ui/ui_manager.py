import customtkinter
from src.ui.components import launch_game, version_switcher, version_adder, mod_list, mod_loader_switches
from src.core.config import Config


class UIManager:
    """
    Handles all UI Presentation and Management
    """

    def __init__(self):
        self.config = Config()

        customtkinter.set_appearance_mode(self.config.config_data["ui"]["appearance_mode"])
        customtkinter.set_default_color_theme(self.config.config_data["ui"]["color_theme"])

        self.root = customtkinter.CTk()
        self.root.geometry(self.config.config_data["ui"]["dimensions"])
        self.root.title("Jedixxx's Mod Manager")
        self.root.resizable(False, False)
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.updating_objects = []
        self.refresh_time = self.config.config_data["misc"]["refresh_time"]

    def update_loop(self):
        for object_to_update in self.updating_objects:
            object_to_update.update_function()
        self.root.after(self.refresh_time, self.update_loop)

    def load_ui(self):
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        title = customtkinter.CTkLabel(master=self.frame, text="Jedixxx's Mod Manager",
                                       font=("Arial", 30, "bold"))
        title.pack(pady=12, padx=10)

        mod_list_controller = mod_list.ModList(master=self.frame, scrollable_width=600, scrollable_height=700, scrollable_x=50, scrollable_y=100)
        mod_list_controller.load()
        self.updating_objects.append(mod_list_controller)

        launch_button_controller = launch_game.LaunchGame(master=self.frame, width=400, height=150, x=1000, y=660, text_size=40, update_mod_position_function=mod_list_controller.mod_file_manager.update_mod_positions)
        launch_button_controller.load()
        self.updating_objects.append(launch_button_controller)

        version_switcher_controller = version_switcher.VersionSwitcher(master=self.frame, width=340, height=50, x=1060, y=600, launch_button_controller=launch_button_controller)
        version_switcher_controller.load()
        self.updating_objects.append(version_switcher_controller)

        version_adder_controller = version_adder.VersionAdder(master=self.frame, width=50, height=50, x=1000, y=600, root=self.root)
        version_adder_controller.load()

        mod_loader_switches_controller = mod_loader_switches.ModLoaderSwitches(master=self.frame, x=708, y=660, width=250, height=150)
        mod_loader_switches_controller.load()


