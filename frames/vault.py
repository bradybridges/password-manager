from tkinter import ttk


class Vault(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.label = ttk.Label(self, text="Hello").pack()
