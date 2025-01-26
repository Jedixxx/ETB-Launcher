import customtkinter
from src.file_manager.savefile_il_reset import SaveFileReset
from tkinter import filedialog
import time
import os


class QuickResetUI:
    def __init__(self, ui_manager, x, y, width, height):
        self.master = ui_manager.frame
        self.save_file_reset = SaveFileReset()
        self.x, self.y = x, y

        self.master_widget = customtkinter.CTkFrame(master=self.master, width=width, height=height)
        self.master_widget.grid_columnconfigure(0, weight=1)
        self.master_widget.grid_columnconfigure(1, weight=1)
        self.master_widget.grid_columnconfigure(2, weight=1)
        self.master_widget.grid_columnconfigure(3, weight=1)
        self.master_widget.grid_propagate(False)

        self.title = customtkinter.CTkLabel(master=self.master_widget, text="Quick Reset",
                                            font=("Arial", 25, "bold"))

        self.savegame_path_entry = customtkinter.CTkEntry(master=self.master_widget, width=300, height=50,
                                                          placeholder_text="Path to base savefile")

        self.start_listening_button = customtkinter.CTkButton(master=self.master_widget, text="Start", width=150,
                                                              height=60,
                                                              font=("Arial", 20, "bold"), fg_color="gray",
                                                              state="disabled", command=self.switch_listen_mode)
        self.is_listening = False

        self.browse_button = customtkinter.CTkButton(master=self.master_widget, text="📁", width=50, height=50,
                                                     font=("Arial", 30),
                                                     command=lambda: self.browse_for_savegame(self.savegame_path_entry,
                                                                                              self.start_listening_button))

        self.set_keybind_button = customtkinter.CTkButton(master=self.master_widget, text="No Keybind", width=150,
                                                          height=60,
                                                          font=("Arial", 20, "bold"), fg_color="gray",
                                                          command=self.set_keybind)
        self.call_set_keybind = False
        self.visual_keybind = None
        self.update_function = self.update_keybind_display

    def update_keybind_display(self):
        if self.call_set_keybind:
            self.call_set_keybind = False
            self.save_file_reset.set_keybind()
        if self.save_file_reset.keybind != self.visual_keybind:
            self.visual_keybind = self.save_file_reset.keybind
            self.set_keybind_button.configure(text=self.visual_keybind)

    def set_keybind(self):
        self.set_keybind_button.configure(text="...")
        self.call_set_keybind = True

    def switch_listen_mode(self):
        if not self.is_listening:
            self.save_file_reset.start_listen(self.savegame_path_entry.get())
            self.start_listening_button.configure(fg_color="red", text="Stop")
        else:
            self.save_file_reset.stop_listen()
            self.start_listening_button.configure(fg_color="green", text="Start")

        self.is_listening = not self.is_listening

    @staticmethod
    def browse_for_savegame(savegame_entry, listen_button):
        version_path = filedialog.askopenfilename(filetypes=[("SaveGame files", "*.sav")])

        if version_path:
            savegame_entry.delete(0, customtkinter.END)
            savegame_entry.insert(0, version_path)
            if os.path.exists(version_path) or os.path.basename(version_path)[-4:] != ".sav":
                listen_button.configure(state="default", fg_color="green")

    def load(self):
        self.master_widget.place(x=self.x, y=self.y)
        self.title.grid(row=0, column=0, columnspan=4, pady=10)
        self.savegame_path_entry.grid(row=1, column=0, columnspan=3)
        self.browse_button.grid(row=1, column=3)
        self.start_listening_button.grid(row=2, column=2, columnspan=2, pady=20, padx=10)
        self.set_keybind_button.grid(row=2, column=0, columnspan=2)
