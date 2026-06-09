from tkinter import Tk, Toplevel


def get_window_info(
    Tk: Tk | Toplevel, window_width: int, window_height: int
) -> dict[str, int]:
    # Screen dimensions
    screen_width = Tk.winfo_screenwidth()
    screen_height = Tk.winfo_screenheight()

    # Center of screen coordinates
    screen_x_center = int(screen_width / 2)
    screen_y_center = int(screen_height / 2)
    window_x_center = int(screen_x_center - (window_width / 2))
    window_y_center = int(screen_y_center - (window_height / 2))

    return {
        "screen_width": screen_width,
        "screen_height": screen_height,
        "screen_x_center": screen_x_center,
        "screen_y_center": screen_y_center,
        "window_x_center": window_x_center,
        "window_y_center": window_y_center,
    }
