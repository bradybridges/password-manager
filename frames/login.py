import tkinter as tk
from tkinter import ttk

from frames.vault import Vault


class Login(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        # Password label and input
        def validate_password(var, index, mode):
            current_entry = self.password_text.get()

            if current_entry:
                self.button.state(["!disabled"])
            else:
                self.button.state(["disabled"])

        # Label
        self.password_label = ttk.Label(self, text="Master Password")
        self.password_label.pack(pady=2)

        # Entry observer
        self.password_text = tk.StringVar()
        self.password_text.trace_add("write", validate_password)

        # Password entry
        self.password_entry = ttk.Entry(self, show="*", textvariable=self.password_text)
        self.password_entry.pack(pady=5, padx=5)

        # Button
        self.button = ttk.Button(self, text="Unlock", command=self.handle_click)
        self.button.state(["disabled"])
        self.button.pack(ipadx=5, ipady=5)

    def handle_click(self):
        self.controller.show_frame(Vault)
