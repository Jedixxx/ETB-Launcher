import customtkinter

from src.mod_loader_manager.interpose_manager import InterposeManager


class ModLoaderSwitches:
    def __init__(self, master, x, y, width, height):
        interpose_manager = InterposeManager()

        self.x, self.y = x, y

        self.master_widget = customtkinter.CTkFrame(master=master, width=width, height=height)
        self.master_widget.pack_propagate(False)  # Prevent frame from resizing itself

        self.title = customtkinter.CTkLabel(master=self.master_widget, text="Mod Loaders",
                                            font=("Arial", 25, "bold"))

        self.ue4ss_switch = customtkinter.CTkSwitch(master=self.master_widget, text="UE4SS", font=("Arial", 20))
        self.interpose_switch = customtkinter.CTkSwitch(master=self.master_widget, text="Interpose", font=("Arial", 20), command=interpose_manager.switch, variable=interpose_manager.interpose_enabled)

    def load(self):
        self.master_widget.place(x=self.x, y=self.y)
        self.title.pack(pady=10)
        self.ue4ss_switch.pack(pady=10, padx=25, anchor="w")
        self.interpose_switch.pack(pady=10, padx=25, anchor="w")
