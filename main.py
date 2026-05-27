import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from frames.create_vault import CreateVault
from frames.login import Login
from frames.vault import Vault
from utils.vault_manager import VaultCorruptError, VaultManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Window dimensions
        window_width = 600
        window_height = 400
        window_x_position = int((screen_width / 2) - (window_width / 2))
        window_y_position = int((screen_height / 2) - (window_height / 2))

        window_geometry = (
            f"{window_width}x{window_height}+{window_x_position}+{window_y_position}"
        )

        # Window setup
        self.title("Password Manager")
        self.geometry(window_geometry)
        self.resizable(False, False)

        # Init vault manager
        self.vault_manager = VaultManager()

        # Menubar
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import Vault", command=self.import_vault)
        file_menu.add_command(label="Export Vault", command=self.export_vault)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Container setup
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Frames setup
        self.frames = {}
        for name, FrameClass in (("Login", Login), ("CreateVault", CreateVault), ("Vault", Vault)):
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, name, **kwargs):
        frame = self.frames[name]
        if kwargs:
            frame.load(**kwargs)
        elif hasattr(frame, "load"):
            frame.load()
        frame.tkraise()

    def import_vault(self):
        path = filedialog.askopenfilename(
            title="Import Vault",
            filetypes=[("Vault files", "*.vault")],
        )
        if not path:
            return
        try:
            imported_name = self.vault_manager.import_vault(path)
            messagebox.showinfo("Vault Imported", f'Vault "{imported_name}" imported successfully.')
            if self.frames["Login"].winfo_ismapped() or True:
                self.show_frame("Login")
        except VaultCorruptError:
            messagebox.showerror("Import Failed", "The selected file is not a valid vault.")

    def export_vault(self):
        vault_frame = self.frames["Vault"]
        if not vault_frame.vault_name:
            messagebox.showinfo("No Vault Open", "Open a vault first before exporting.")
            return
        path = filedialog.asksaveasfilename(
            title="Export Vault",
            initialfile=f"{vault_frame.vault_name}.vault",
            defaultextension=".vault",
            filetypes=[("Vault files", "*.vault")],
        )
        if not path:
            return
        self.vault_manager.export(vault_frame.vault_name, path)
        messagebox.showinfo("Vault Exported", f'Vault exported to "{path}".')


if __name__ == "__main__":
    app = App()
    app.mainloop()
