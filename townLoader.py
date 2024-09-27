import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip
import json
import os


class LoadoutManager:
    def __init__(self, root):
        self.root = root
        self.root.title("townLoader")
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.root.resizable(False, False)  # Disable resizing

        self.loadouts_file = "loadouts/loadouts.json"  # File to save/load loadouts
        self.loadouts = {}  # Stores loadouts as {name: [gun strings]}
        self.current_loadout = None

        # Create dark-themed GUI components
        self.create_widgets()

        # Load existing loadouts if available
        self.load_loadouts()  # Now called after widgets are created

    def create_widgets(self):
        # Loadout selection (dark theme)
        self.loadout_listbox = tk.Listbox(
            self.root, bg="#333333", fg="#FFFFFF", selectbackground="#555555"
        )
        self.loadout_listbox.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
        self.loadout_listbox.bind("<<ListboxSelect>>", self.load_loadout)

        # Buttons for loadout management (dark theme)
        button_bg = "#444444"
        button_fg = "#FFFFFF"

        self.add_loadout_btn = tk.Button(
            self.root,
            text="New Loadout",
            command=self.new_loadout,
            bg=button_bg,
            fg=button_fg,
        )
        self.add_loadout_btn.grid(row=0, column=1, padx=10, pady=5)

        self.add_gun_btn = tk.Button(
            self.root, text="Add Gun", command=self.add_gun, bg=button_bg, fg=button_fg
        )
        self.add_gun_btn.grid(row=1, column=1, padx=10, pady=5)

        self.remove_gun_btn = tk.Button(
            self.root,
            text="Remove Gun",
            command=self.remove_gun,
            bg=button_bg,
            fg=button_fg,
        )
        self.remove_gun_btn.grid(row=2, column=1, padx=10, pady=5)

        self.copy_loadout_btn = tk.Button(
            self.root,
            text="Copy Loadout",
            command=self.copy_loadout,
            bg=button_bg,
            fg=button_fg,
        )
        self.copy_loadout_btn.grid(row=3, column=1, padx=10, pady=5)

        # Listbox for displaying guns in the selected loadout (dark theme, selectable)
        self.gun_listbox = tk.Listbox(
            self.root,
            height=10,
            width=40,
            bg="#333333",
            fg="#FFFFFF",
            selectbackground="#555555",
        )
        self.gun_listbox.grid(row=0, column=2, rowspan=4, padx=10, pady=10)
        self.gun_listbox.bind(
            "<Double-Button-1>", self.edit_gun
        )  # Double-click to edit gun

    def new_loadout(self):
        name = simpledialog.askstring("New Loadout", "Enter the loadout name:")
        if name:
            self.loadouts[name] = []
            self.update_loadout_list()
            self.save_loadouts()  # Save after new loadout is created

    def add_gun(self):
        if self.current_loadout is None:
            messagebox.showwarning(
                "No Loadout", "Please select or create a loadout first."
            )
            return

        gun = simpledialog.askstring(
            "Add Gun",
            "Enter the gun and attachments in format 'gun+attachment1+attachment2':",
        )
        if gun:
            self.loadouts[self.current_loadout].append(gun)
            self.update_gun_list()
            self.save_loadouts()  # Save after a gun is added

    def remove_gun(self):
        if self.current_loadout is None:
            messagebox.showwarning("No Loadout", "Please select a loadout first.")
            return

        selected_gun_index = self.gun_listbox.curselection()
        if selected_gun_index:
            selected_gun = self.gun_listbox.get(selected_gun_index)
            self.loadouts[self.current_loadout].remove(selected_gun)
            self.update_gun_list()
            self.save_loadouts()  # Save after a gun is removed
        else:
            messagebox.showwarning("No Selection", "Please select a gun to remove.")

    def copy_loadout(self):
        if self.current_loadout is None:
            messagebox.showwarning("No Loadout", "Please select a loadout first.")
            return

        # Create the full command string starting with !sts
        loadout_str = "!sts " + " ".join(self.loadouts[self.current_loadout])
        pyperclip.copy(loadout_str)
        messagebox.showinfo("Copied", "Loadout copied to clipboard!")

    def load_loadout(self, event):
        if self.loadout_listbox.curselection():
            index = self.loadout_listbox.curselection()[0]
            self.current_loadout = self.loadout_listbox.get(index)
            self.update_gun_list()

    def update_loadout_list(self):
        self.loadout_listbox.delete(0, tk.END)
        for loadout in self.loadouts:
            self.loadout_listbox.insert(tk.END, loadout)

    def update_gun_list(self):
        self.gun_listbox.delete(0, tk.END)
        if self.current_loadout:
            for gun in self.loadouts[self.current_loadout]:
                self.gun_listbox.insert(tk.END, gun)

    def edit_gun(self, event):
        if self.current_loadout is None:
            messagebox.showwarning("No Loadout", "Please select a loadout first.")
            return

        selected_gun_index = self.gun_listbox.curselection()
        if selected_gun_index:
            selected_gun = self.gun_listbox.get(selected_gun_index)
            new_gun = simpledialog.askstring(
                "Edit Gun", f"Edit the gun and attachments:", initialvalue=selected_gun
            )
            if new_gun:
                self.loadouts[self.current_loadout][selected_gun_index[0]] = new_gun
                self.update_gun_list()
                self.save_loadouts()  # Save after a gun is edited

    def save_loadouts(self):
        """Saves the loadouts to a JSON file."""
        os.makedirs(
            os.path.dirname(self.loadouts_file), exist_ok=True
        )  # Ensure directory exists
        with open(self.loadouts_file, "w") as f:
            json.dump(self.loadouts, f, indent=4)

    def load_loadouts(self):
        """Loads the loadouts from a JSON file if it exists."""
        if os.path.exists(self.loadouts_file):
            with open(self.loadouts_file, "r") as f:
                self.loadouts = json.load(f)
            self.update_loadout_list()


if __name__ == "__main__":
    root = tk.Tk()

    # Set window icon
    root.iconbitmap(
        "res/icon2.ico"
    )  # Replace with the path to your .ico file if necessary

    app = LoadoutManager(root)
    root.mainloop()
