import customtkinter
import src.ui.logic
from src.core.config import Config

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class UIManager():
    """
    Handles all UI Presentation and Management
    """

    def __init__(self):
        self.config = Config()
        self.root = customtkinter.CTk()
        self.root.geometry("1536x864")
        self.frame = customtkinter.CTkFrame(master=self.root)

    def load_ui(self):
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        title = customtkinter.CTkLabel(master=self.frame, text="Jedixxx's Mod Manager",
                                       font=("Arial", 30, "bold"))
        title.pack(pady=12, padx=10)
