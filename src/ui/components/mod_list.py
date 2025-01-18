import os

import customtkinter

from src.file_manager.mod_file_manager import ModFileManager


class ModList:
    def __init__(self, ui_manager, scrollable_width, scrollable_height, scrollable_x, scrollable_y):
        self.master = ui_manager.frame
        self.mod_file_manager = ModFileManager()

        self.scrollable_width = scrollable_width
        self.scrollable_x = scrollable_x
        self.scrollable_y = scrollable_y

        self.deselect_all_button = customtkinter.CTkButton(self.master, width=round(scrollable_width / 6), height=25,
                                                           text="Deselect All",
                                                           command=self.deselect_all)

        self.refresh_button = customtkinter.CTkButton(self.master, width=25, height=25,
                                                      text="⭮",
                                                      command=self.refresh_mod_list)

        self.search_bar = customtkinter.CTkEntry(self.master, width=round(scrollable_width / 1.5), height=25,
                                                 placeholder_text="Search for Mod")

        self.scrollable_mod_list = customtkinter.CTkScrollableFrame(self.master, width=scrollable_width,
                                                                    height=scrollable_height)

        self.mod_file_manager.load_local_mods()
        self.mod_checkbox_pairs = []
        for mod in self.mod_file_manager.loaded_mods:
            self.mod_checkbox_pairs.append(
                (mod, customtkinter.CTkCheckBox(master=self.scrollable_mod_list, text=mod.name, variable=mod.activated,
                                                onvalue=True, offvalue=False, font=("Arial", 20), checkbox_width=30,
                                                checkbox_height=30)))

        self.update_function = self.update_mod_list
        self.prev_filtered_checkbox_pairs = None

    def load(self):
        self.search_bar.place(x=self.scrollable_x, y=self.scrollable_y - 30)
        self.deselect_all_button.place(
            x=self.scrollable_x + self.scrollable_width - round(self.scrollable_width / 6) + 10,
            y=self.scrollable_y - 30)
        self.refresh_button.place(x=self.scrollable_x + round(self.scrollable_width / 1.5) + 5,
                                  y=self.scrollable_y - 30)
        self.scrollable_mod_list.place(x=self.scrollable_x, y=self.scrollable_y)
        for mod_info in self.mod_checkbox_pairs:
            _, mod_checkbox = mod_info
            mod_checkbox.pack(anchor="w", pady=6)

    def refresh_mod_list(self):
        for mod_info in self.mod_checkbox_pairs:
            _, mod_checkbox = mod_info
            mod_checkbox.pack_forget()

        self.mod_file_manager.load_local_mods()
        self.mod_checkbox_pairs.clear()
        for mod in self.mod_file_manager.loaded_mods:
            self.mod_checkbox_pairs.append(
                (mod, customtkinter.CTkCheckBox(master=self.scrollable_mod_list, text=mod.name, variable=mod.activated,
                                                onvalue=True, offvalue=False, font=("Arial", 20), checkbox_width=30,
                                                checkbox_height=30)))

        self.search_bar.delete(0, "end")
        self.master.focus()

        for mod_info in self.mod_checkbox_pairs:
            m, mod_checkbox = mod_info
            mod_checkbox.pack(anchor="w", pady=6)

    def redraw_mod_list(self, filtered_checkboxes):
        # Delete all checkboxes
        for mod_info in self.mod_checkbox_pairs:
            _, mod_checkbox = mod_info
            mod_checkbox.pack_forget()

        # Redraw filtered checkboxes
        for mod_info in filtered_checkboxes:
            m, mod_checkbox = mod_info
            mod_checkbox.pack(anchor="w", pady=6)

    def update_mod_list(self):
        filtered_checkbox_pairs = []

        for mod_info in self.mod_checkbox_pairs:
            mod, mod_checkbox = mod_info

            # Update for search terms
            if self.search_bar.get().lower() in mod.name.lower():
                filtered_checkbox_pairs.append(mod_info)

            # Prioritise favourites

        if filtered_checkbox_pairs != self.prev_filtered_checkbox_pairs:
            self.prev_filtered_checkbox_pairs = filtered_checkbox_pairs
            self.redraw_mod_list(filtered_checkbox_pairs)

    def deselect_all(self):
        for mod_info in self.mod_checkbox_pairs:
            mod, _ = mod_info
            mod.activated.set(False)
