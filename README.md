# Password Manager

A simple desktop password manager built with Python and tkinter.

## Features

- Create and manage multiple encrypted vaults
- Store credentials with title, username, password, URL, and notes
- AES encryption via PBKDF2 key derivation (600,000 iterations, SHA-256)
- Import and export vaults as portable `.vault` files
- Password show/hide toggle and one-click copy

## Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv)

## Getting Started

Install dependencies and run the app:

```bash
uv run main.py
```

## Usage

1. Launch the app and create a new vault with a master password.
2. Unlock the vault to view and manage your credentials.
3. Use the **+ Add** button to create entries, or select an existing entry to edit or delete it.
4. Use **File > Export Vault** to back up a vault, or **File > Import Vault** to restore one.

## Building

To produce a standalone `Password Manager.app` that runs without Python or uv installed:

```bash
uv run pyinstaller -y password_manager.spec
```

The app is output to `dist/Password Manager.app`. You can move it to `/Applications` or distribute it directly. The `build/` and `dist/` directories are not committed to version control.

## Vault Storage

Vaults are stored locally on disk at a platform-specific path:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Password Manager/vaults/` |
| Windows | `%APPDATA%\Password Manager\vaults\` |
| Linux | `$XDG_DATA_HOME/password-manager/vaults/` |

Each `.vault` file is a JSON document containing a base64-encoded salt and Fernet-encrypted credentials. The master password never leaves your machine.
