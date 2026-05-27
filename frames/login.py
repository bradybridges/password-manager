import tkinter as tk
from tkinter import messagebox, ttk

from utils.vault_manager import VaultNotFoundError, VaultWrongPasswordError


class Login(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self._build_no_vaults_ui()
        self._build_unlock_ui()

    def load(self):
        vaults = self.controller.vault_manager.list()
        if vaults:
            self._show_unlock(vaults)
        else:
            self._show_no_vaults()

    # --- no-vaults UI ---

    def _build_no_vaults_ui(self):
        self.no_vaults_frame = ttk.Frame(self)
        ttk.Label(self.no_vaults_frame, text="No vaults found.").pack(pady=(60, 10))
        ttk.Button(
            self.no_vaults_frame,
            text="Create Your First Vault",
            command=lambda: self.controller.show_frame("CreateVault"),
        ).pack(ipadx=5, ipady=5)

    # --- unlock UI ---

    def _build_unlock_ui(self):
        self.unlock_frame = ttk.Frame(self)

        ttk.Label(self.unlock_frame, text="Vault").pack(pady=(40, 2))
        self.vault_var = tk.StringVar()
        self.vault_dropdown = ttk.Combobox(
            self.unlock_frame, textvariable=self.vault_var, state="readonly"
        )
        self.vault_dropdown.pack(pady=2, padx=5)

        def validate(_var, _index, _mode):
            if self.password_text.get():
                self.unlock_button.state(["!disabled"])
            else:
                self.unlock_button.state(["disabled"])

        ttk.Label(self.unlock_frame, text="Master Password").pack(pady=(8, 2))
        self.password_text = tk.StringVar()
        self.password_text.trace_add("write", validate)
        ttk.Entry(self.unlock_frame, show="*", textvariable=self.password_text).pack(pady=2, padx=5)

        self.unlock_button = ttk.Button(self.unlock_frame, text="Unlock", command=self.handle_click)
        self.unlock_button.state(["disabled"])
        self.unlock_button.pack(pady=10, ipadx=5, ipady=5)

    def _show_unlock(self, vaults):
        self.no_vaults_frame.place_forget()
        self.vault_dropdown["values"] = vaults
        if vaults:
            self.vault_var.set(vaults[0])
        self.password_text.set("")
        self.unlock_frame.place(relx=0.5, rely=0.5, anchor="center")

    def _show_no_vaults(self):
        self.unlock_frame.place_forget()
        self.no_vaults_frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- actions ---

    def handle_click(self):
        name = self.vault_var.get()
        password = self.password_text.get()
        try:
            credentials = self.controller.vault_manager.open(name, password)
            self.password_text.set("")
            self.controller.show_frame("Vault", credentials=credentials, vault_name=name, password=password)
        except VaultWrongPasswordError:
            messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")
        except VaultNotFoundError:
            messagebox.showerror("Vault Not Found", f'No vault named "{name}" was found.')
