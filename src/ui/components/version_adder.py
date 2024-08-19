import customtkinter
import tkinter
from tkinter import filedialog

from src.etb_version_controller.version_loader import VersionLoader


class VersionAdder:
    def __init__(self, master, width, height, x, y, root):
        self.version_loader = VersionLoader()
        self.x, self.y = x, y

        self.root = root
        self.version_add_button = customtkinter.CTkButton(master=master, width=width, height=height, text="+",
                                                          command=self.open_add_version_popup, font=("Arial", 30))

    def load(self):
        self.version_add_button.place(x=self.x, y=self.y)

    def open_add_version_popup(self):
        add_version_popup = tkinter.Toplevel(self.root)
        add_version_popup.geometry("500x210")
        add_version_popup.title("Load Local Version")
        add_version_popup.configure(background="gray18")
        add_version_popup.resizable(False, False)

        version_path_entry = customtkinter.CTkEntry(add_version_popup, width=340, height=50,
                                                    placeholder_text="Path to version files")
        version_path_entry.place(x=50, y=20)

        version_entry = customtkinter.CTkEntry(add_version_popup, width=400, height=50,
                                               placeholder_text="Version of selected folder")
        version_entry.place(x=50, y=80)

        add_button = customtkinter.CTkButton(add_version_popup, text="Add Version", width=400, height=50,
                                             command=lambda: self.load_local_version(version_path_entry.get(),
                                                                                     version_entry.get()))
        add_button.place(x=50, y=140)

        browse_button = customtkinter.CTkButton(add_version_popup, text="📁", width=50, height=50, font=("Arial", 30),
                                                command=lambda: self.browse_for_version_files(version_path_entry,
                                                                                              version_entry))
        browse_button.place(x=400, y=20)

    @staticmethod
    def browse_for_version_files(version_path_entry, version_entry):
        version_path = filedialog.askdirectory()
        if version_path:
            # ADD CHECK HERE

            version_path_entry.delete(0, customtkinter.END)
            version_path_entry.insert(0, version_path)

            detected_version = VersionLoader.get_game_version_from_bytes(version_path)
            if detected_version:
                version_entry.delete(0, customtkinter.END)
                version_entry.insert(0, f"{detected_version} (Auto-detected)")

    def load_local_version(self, filepath, version):
        # Need to add CHECKS

        raw_version = version.replace(" (Auto-detected)", "")
        self.version_loader.load_local_version(filepath, raw_version)
