import tkinter as tk
from tkinter import messagebox, ttk


class CreateVault(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        def validate(_var, _index, _mode):
            name = self.name_text.get()
            password = self.password_text.get()
            confirm = self.confirm_text.get()
            if name and password and password == confirm:
                self.create_button.state(["!disabled"])
            else:
                self.create_button.state(["disabled"])

        ttk.Label(self, text="Create Vault").pack(pady=(20, 10))

        ttk.Label(self, text="Vault Name").pack()
        self.name_text = tk.StringVar()
        self.name_text.trace_add("write", validate)
        ttk.Entry(self, textvariable=self.name_text).pack(pady=2, padx=5)

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
        except Exception as e:
            messagebox.showerror("Error", f"Could not create vault: {e}")

    def handle_back(self):
        self._reset()
        self.controller.show_frame("Login")

    def _reset(self):
        self.name_text.set("")
        self.password_text.set("")
        self.confirm_text.set("")
