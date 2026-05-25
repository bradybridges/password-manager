import tkinter as tk
from tkinter import ttk

from frames.login import Login
from frames.vault import Vault


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

        # Menubar
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Container setup
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FrameClass in (Login,Vault):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, frame_class):
        self.frames[frame_class].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
