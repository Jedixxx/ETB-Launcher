import customtkinter
from src.ui.components import launch_game
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
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.updating_objects = []

    def update_loop(self):
        for object_to_update in self.updating_objects:
            object_to_update.update_function()
        self.root.after(1000, self.update_loop)

    def load_ui(self):
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        title = customtkinter.CTkLabel(master=self.frame, text="Jedixxx's Mod Manager",
                                       font=("Arial", 30, "bold"))
        title.pack(pady=12, padx=10)

        launch_button_controller = launch_game.LaunchGame(self.frame, width=400, height=150, x=1000, y=660, text_size=40)
        self.updating_objects.append(launch_button_controller)

