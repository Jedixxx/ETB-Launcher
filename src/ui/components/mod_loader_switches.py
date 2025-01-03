import customtkinter

from src.mod_loader_manager.interpose_manager import InterposeManager
from src.mod_loader_manager.ue4ss_manager import UE4SSManager


class ModLoaderSwitches:
    def __init__(self, master, x, y, width, height):
        self.interpose_manager = InterposeManager()
        self.ue4ss_manager = UE4SSManager()

        self.x, self.y = x, y

        self.master_widget = customtkinter.CTkFrame(master=master, width=width, height=height)
        self.master_widget.pack_propagate(False)  # Prevent frame from resizing itself

        self.title = customtkinter.CTkLabel(master=self.master_widget, text="Mod Loaders",
                                            font=("Arial", 25, "bold"))

        self.ue4ss_switch = customtkinter.CTkSwitch(master=self.master_widget, text="UE4SS", font=("Arial", 20), command=self.ue4ss_manager.switch, variable=self.ue4ss_manager.ue4ss_enabled, state="normal" if self.ue4ss_manager.ue4ss_locally_installed else "disabled")
        self.interpose_switch = customtkinter.CTkSwitch(master=self.master_widget, text="Interpose", font=("Arial", 20), command=self.interpose_manager.switch, variable=self.interpose_manager.interpose_enabled, state="normal" if self.interpose_manager.interpose_locally_installed else "disabled")

    def load(self):
        self.master_widget.place(x=self.x, y=self.y)
        self.title.pack(pady=10)
        self.ue4ss_switch.pack(pady=10, padx=25, anchor="w")
        self.interpose_switch.pack(pady=10, padx=25, anchor="w")