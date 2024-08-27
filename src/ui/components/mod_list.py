import os

import customtkinter

from src.file_manager.mod_file_manager import ModFileManager


class ModList:
    def __init__(self, master, x, y):
        self.mod_file_manager = ModFileManager()

        self.search_bar = customtkinter.CTkEntry(master, width=400, height=25,
                                                 placeholder_text="Search for Mod")

        self.scrollable_mod_list = customtkinter.CTkScrollableFrame(master, width=600, height=700)
        self.mod_file_manager.load_local_mods()
        self.mod_checkbox_pairs = []
        for mod in self.mod_file_manager.loaded_mods:
            self.mod_checkbox_pairs.append(
                (mod, customtkinter.CTkCheckBox(master=self.scrollable_mod_list, text=mod.name, variable=mod.activated,
                                                onvalue=True, offvalue=False, font=("Arial", 20), checkbox_width=30,
                                                checkbox_height=30)))

        self.update_function = self.update_mod_list

    def load(self):
        self.search_bar.place(x=50, y=70)
        self.scrollable_mod_list.place(x=50, y=100)
        for mod_info in self.mod_checkbox_pairs:
            _, mod_checkbox = mod_info
            mod_checkbox.pack(anchor="w", pady=6)

    def redraw_mod_list(self, filtered_checkboxes):
        for mod_info in self.mod_checkbox_pairs:
            _, mod_checkbox = mod_info
            mod_checkbox.pack_forget()

        for mod_info in filtered_checkboxes:
            _, mod_checkbox = mod_info
            mod_checkbox.pack(anchor="w", pady=6)

    def update_mod_list(self):
        filtered_checkbox_pairs = self.mod_checkbox_pairs.copy()

        for mod_info in self.mod_checkbox_pairs:
            mod, mod_checkbox = mod_info

            # Update for search terms
            if self.search_bar.get() != "":
                if self.search_bar.get().lower() not in mod.name.lower():
                    filtered_checkbox_pairs.remove(mod_info)
                    continue

            # Update for user movements/deletion of mods
            if not os.path.isfile(os.path.join("mods", mod.filename)):
                self.mod_checkbox_pairs.remove(mod_info)  # If mod is missing from mod folder then remove it from list
                filtered_checkbox_pairs.remove(mod_info)
                continue

            # Update for filters

        if filtered_checkbox_pairs != self.mod_checkbox_pairs:
            self.redraw_mod_list(filtered_checkbox_pairs)