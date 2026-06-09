import tkinter as tk
from tkinter import messagebox, ttk

from utils.vault_manager import VaultAlreadyExistsError

INVALID_NAME_CHARS = set('/\\:*?"<>|')


def _validate_vault_name(name: str) -> str:
    """Return an error string, or empty string if name is valid."""
    if not name.strip():
        return "Name cannot be blank."
    if any(c in INVALID_NAME_CHARS for c in name):
        bad = ", ".join(sorted(INVALID_NAME_CHARS))
        return f"Name cannot contain: {bad}"
    return ""


class CreateVault(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        def validate(_var, _index, _mode):
            name = self.name_text.get()
            password = self.password_text.get()
            confirm = self.confirm_text.get()
            name_error = _validate_vault_name(name)
            if name_error:
                self.name_error_label.config(text=name_error)
            else:
                self.name_error_label.config(text="")
            if name and not name_error and password and password == confirm:
                self.create_button.state(["!disabled"])
            else:
                self.create_button.state(["disabled"])

        ttk.Label(self, text="Create Vault").pack(pady=(20, 10))

        ttk.Label(self, text="Vault Name").pack()
        self.name_text = tk.StringVar()
        self.name_text.trace_add("write", validate)
        ttk.Entry(self, textvariable=self.name_text).pack(pady=(2, 0), padx=5)
        self.name_error_label = ttk.Label(self, text="", foreground="red")
        self.name_error_label.pack()

        ttk.Label(self, text="Password").pack(pady=(8, 0))
        self.password_text = tk.StringVar()
        self.password_text.trace_add("write", validate)
        ttk.Entry(self, show="*", textvariable=self.password_text).pack(pady=2, padx=5)

        ttk.Label(self, text="Confirm Password").pack(pady=(8, 0))
        self.confirm_text = tk.StringVar()
        self.confirm_text.trace_add("write", validate)
        ttk.Entry(self, show="*", textvariable=self.confirm_text).pack(pady=2, padx=5)

        button_row = ttk.Frame(self)
        button_row.pack(pady=15)

        self.create_button = ttk.Button(button_row, text="Create Vault", command=self.handle_create)
        self.create_button.state(["disabled"])
        self.create_button.pack(side="left", ipadx=5, ipady=5, padx=(0, 8))

        ttk.Button(button_row, text="Back", command=self.handle_back).pack(side="left", ipadx=5, ipady=5)

    def handle_create(self):
        name = self.name_text.get()
        password = self.password_text.get()
        try:
            self.controller.vault_manager.create(name, password)
            self._reset()
            self.controller.show_frame("Login")
        except VaultAlreadyExistsError:
            messagebox.showerror("Vault Already Exists", f'A vault named "{name}" already exists. Choose a different name.')
        except OSError as e:
            messagebox.showerror("Error", f"Could not create vault: {e}")

    def handle_back(self):
        self._reset()
        self.controller.show_frame("Login")

    def _reset(self):
        self.name_text.set("")
        self.password_text.set("")
        self.confirm_text.set("")
        self.name_error_label.config(text="")
