import tkinter as tk
from tkinter import messagebox, ttk


class Vault(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.vault_name = None
        self.password = None
        self.credentials = []
        self._password_visible = False
        self._selected_index = None

        self._build_ui()

    def load(self, credentials, vault_name, password):
        self.credentials = credentials
        self.vault_name = vault_name
        self.password = password
        self._password_visible = False
        self.vault_label.config(text=vault_name)
        self._refresh_list()
        self._clear_detail()

    # --- build ---

    def _build_ui(self):
        # Top bar
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=(8, 4))
        self.vault_label = ttk.Label(top, text="", font=("", 11, "bold"))
        self.vault_label.pack(side="left")
        ttk.Button(top, text="Close Vault", command=self.handle_close).pack(side="right")

        # Main area
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=8, pady=4)

        # Left: list
        left = ttk.Frame(main, width=190)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        scrollbar = ttk.Scrollbar(left, orient="vertical")
        self.listbox = tk.Listbox(left, yscrollcommand=scrollbar.set, selectmode="single", activestyle="none")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        ttk.Separator(main, orient="vertical").pack(side="left", fill="y", padx=4)

        # Right: detail panel
        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)
        self._build_detail(right)

        # Bottom bar
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=8, pady=(4, 8))
        ttk.Button(bottom, text="+ Add", command=self.handle_add).pack(side="left", ipadx=4, ipady=3)
        self.edit_button = ttk.Button(bottom, text="Edit", command=self.handle_edit)
        self.edit_button.pack(side="left", ipadx=4, ipady=3, padx=(6, 0))
        self.edit_button.state(["disabled"])
        self.delete_button = ttk.Button(bottom, text="Delete", command=self.handle_delete)
        self.delete_button.pack(side="right", ipadx=4, ipady=3)
        self.delete_button.state(["disabled"])

    def _build_detail(self, parent):
        self.detail_frame = ttk.Frame(parent)
        self.detail_frame.pack(fill="both", expand=True, padx=8, pady=4)

        self.empty_label = ttk.Label(self.detail_frame, text="Select an entry to view details", foreground="gray")
        self.empty_label.grid(row=0, column=0, columnspan=3, pady=40)

        fields = ("Title", "Username", "Password", "URL", "Notes")
        self.detail_values = {}

        for i, field in enumerate(fields):
            ttk.Label(self.detail_frame, text=f"{field}:", anchor="e", width=10).grid(
                row=i + 1, column=0, sticky="e", pady=3
            )
            val_label = ttk.Label(self.detail_frame, text="", anchor="w", wraplength=220)
            val_label.grid(row=i + 1, column=1, sticky="w", padx=(4, 0))
            self.detail_values[field] = val_label

            if field == "Password":
                btn_frame = ttk.Frame(self.detail_frame)
                btn_frame.grid(row=i + 1, column=2, padx=(6, 0))
                self.show_btn = ttk.Button(btn_frame, text="Show", width=5, command=self._toggle_password)
                self.show_btn.pack(side="left")
                ttk.Button(btn_frame, text="Copy", width=5, command=self._copy_password).pack(side="left", padx=(4, 0))

        for i in range(1, len(fields) + 1):
            self.detail_frame.grid_rowconfigure(i, weight=0)
        self.detail_frame.grid_columnconfigure(1, weight=1)

    # --- list management ---

    def _refresh_list(self, preserve_index=None):
        self.listbox.delete(0, "end")
        for cred in self.credentials:
            self.listbox.insert("end", cred.get("title", "(no title)"))
        if preserve_index is not None and preserve_index < len(self.credentials):
            self.listbox.selection_set(preserve_index)
            self.listbox.event_generate("<<ListboxSelect>>")

    def _on_select(self, _event):
        selection = self.listbox.curselection()
        if not selection:
            return
        self._selected_index = selection[0]
        cred = self.credentials[self._selected_index]
        self._password_visible = False
        self._populate_detail(cred)
        self.edit_button.state(["!disabled"])
        self.delete_button.state(["!disabled"])

    def _populate_detail(self, cred):
        self.empty_label.grid_remove()
        self.detail_values["Title"].config(text=cred.get("title", ""))
        self.detail_values["Username"].config(text=cred.get("username", ""))
        self.detail_values["Password"].config(text="•" * len(cred.get("password", "")))
        self.detail_values["URL"].config(text=cred.get("url", ""))
        self.detail_values["Notes"].config(text=cred.get("notes", ""))
        self.show_btn.config(text="Show")
        for label in self.detail_values.values():
            label.grid()

    def _clear_detail(self):
        self.empty_label.grid()
        for label in self.detail_values.values():
            label.config(text="")
        self._selected_index = None
        self.edit_button.state(["disabled"])
        self.delete_button.state(["disabled"])

    # --- password show/hide/copy ---

    def _toggle_password(self):
        if self._selected_index is None:
            return
        cred = self.credentials[self._selected_index]
        raw = cred.get("password", "")
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.detail_values["Password"].config(text=raw)
            self.show_btn.config(text="Hide")
        else:
            self.detail_values["Password"].config(text="•" * len(raw))
            self.show_btn.config(text="Show")

    def _copy_password(self):
        if self._selected_index is None:
            return
        raw = self.credentials[self._selected_index].get("password", "")
        self.clipboard_clear()
        self.clipboard_append(raw)

    # --- CRUD actions ---

    def handle_add(self):
        self._open_credential_dialog()

    def handle_edit(self):
        if self._selected_index is None:
            return
        self._open_credential_dialog(existing=self.credentials[self._selected_index])

    def handle_delete(self):
        if self._selected_index is None:
            return
        title = self.credentials[self._selected_index].get("title", "this entry")
        if not messagebox.askyesno("Delete Entry", f'Delete "{title}"? This cannot be undone.'):
            return
        self.credentials.pop(self._selected_index)
        self.controller.vault_manager.save(self.vault_name, self.password, self.credentials)
        self._clear_detail()
        self._refresh_list()

    def handle_close(self):
        self.credentials = []
        self.vault_name = None
        self.password = None
        self._clear_detail()
        self.controller.show_frame("Login")

    # --- shared add/edit dialog ---

    def _open_credential_dialog(self, existing=None):
        dialog = tk.Toplevel(self)
        dialog.title("Edit Entry" if existing else "Add Entry")
        dialog.resizable(False, False)
        dialog.grab_set()

        fields = ("Title", "Username", "Password", "URL", "Notes")
        vars_ = {}

        for i, field in enumerate(fields):
            ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, sticky="e", padx=(12, 4), pady=4)
            var = tk.StringVar(value=existing.get(field.lower(), "") if existing else "")
            show = "*" if field == "Password" else ""
            ttk.Entry(dialog, textvariable=var, show=show, width=30).grid(row=i, column=1, padx=(0, 12), pady=4)
            vars_[field.lower()] = var

        save_btn = ttk.Button(dialog, text="Save", command=lambda: self._save_credential(dialog, vars_, existing))
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=(8, 12))

        def validate(*_):
            if vars_["title"].get():
                save_btn.state(["!disabled"])
            else:
                save_btn.state(["disabled"])

        vars_["title"].trace_add("write", validate)
        validate()

    def _save_credential(self, dialog, vars_, existing):
        data = {k: v.get() for k, v in vars_.items()}
        if existing:
            for cred in self.credentials:
                if cred["id"] == existing["id"]:
                    cred.update(data)
                    break
            new_index = self._selected_index
        else:
            cred = self.controller.vault_manager.new_credential(**data)
            self.credentials.append(cred)
            new_index = len(self.credentials) - 1

        self.controller.vault_manager.save(self.vault_name, self.password, self.credentials)
        dialog.destroy()
        self._refresh_list(preserve_index=new_index)
