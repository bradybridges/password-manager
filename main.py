import tkinter as tk
from tkinter import ttk

from frames.login_frame import LoginFrame


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

        # Set window dimensions
        window_geometry = (
            f"{window_width}x{window_height}+{window_x_position}+{window_y_position}"
        )

        # Window setup
        self.title("Password Manager")
        self.geometry(window_geometry)
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    LoginFrame(app)
    app.mainloop()
