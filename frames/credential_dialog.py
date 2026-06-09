import tkinter as tk
from tkinter import ttk

from utils.window import get_window_info


def open_credential_dialog(parent, *, vault_manager, credentials, vault_name, password, existing=None, on_save):
    """
    Open a modal add/edit dialog for a single credential.

    on_save(new_index) is called after a successful save so the caller can
    refresh its list and restore the selection.
    """
    dialog_width = 400
    dialog_height = 250
    dialog = tk.Toplevel(parent)
    dialog_info = get_window_info(dialog, dialog_width, dialog_height)
    dialog_geometry = f"{dialog_width}x{dialog_height}+{dialog_info['window_x_center']}+{dialog_info['window_y_center']}"
    dialog.geometry(dialog_geometry)
    dialog.title("Edit Entry" if existing else "Add Entry")
    dialog.resizable(False, False)
    dialog.grab_set()
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    fields = ("Title", "Username", "Password", "URL", "Notes")
    field_vars = {}

    for i, field in enumerate(fields):
        ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, sticky="e", padx=(12, 4), pady=4)
        var = tk.StringVar(value=existing.get(field.lower(), "") if existing else "")
        show = "*" if field == "Password" else ""
        ttk.Entry(dialog, textvariable=var, show=show, width=30).grid(row=i, column=1, padx=(0, 12), pady=4)
        field_vars[field.lower()] = var

    def save():
        data = {k: v.get() for k, v in field_vars.items()}
        if existing:
            for cred in credentials:
                if cred["id"] == existing["id"]:
                    cred.update(data)
                    break
            new_index = next((i for i, c in enumerate(credentials) if c["id"] == existing["id"]), None)
        else:
            cred = vault_manager.new_credential(**data)
            credentials.append(cred)
            new_index = len(credentials) - 1

        vault_manager.save(vault_name, password, credentials)
        dialog.destroy()
        on_save(new_index)

    save_btn = ttk.Button(dialog, text="Save", command=save)
    save_btn.grid(row=len(fields), column=0, columnspan=2, pady=(8, 12))

    def validate(*_):
        if field_vars["title"].get():
            save_btn.state(["!disabled"])
        else:
            save_btn.state(["disabled"])

    field_vars["title"].trace_add("write", validate)
    validate()
