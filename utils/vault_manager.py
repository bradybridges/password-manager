import base64
import json
import os
import platform
import shutil
import uuid
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _resolve_vaults_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home()))
        return base / "Password Manager" / "vaults"
    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Password Manager" / "vaults"
    else:
        xdg = os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
        return Path(xdg) / "password-manager" / "vaults"


VAULTS_DIR = _resolve_vaults_dir()
ITERATIONS = 600_000
SALT_BYTES = 16
REQUIRED_KEYS = {"salt", "iterations", "data"}


class VaultError(Exception):
    pass

class VaultNotFoundError(VaultError):
    pass

class VaultWrongPasswordError(VaultError):
    pass

class VaultCorruptError(VaultError):
    pass


class VaultManager:
    def __init__(self):
        VAULTS_DIR.mkdir(parents=True, exist_ok=True)

    def create(self, name: str, password: str) -> None:
        salt = os.urandom(SALT_BYTES)
        fernet = self._make_fernet(password, salt)
        self._write(self._vault_path(name), salt, ITERATIONS, self._encrypt(fernet, []))

    def open(self, name: str, password: str) -> list:
        path = self._vault_path(name)
        if not path.exists():
            raise VaultNotFoundError(name)
        payload = self._read(path)
        salt = base64.b64decode(payload["salt"])
        fernet = self._make_fernet(password, salt, payload["iterations"])
        return self._decrypt(fernet, payload["data"].encode())

    def save(self, name: str, password: str, credentials: list) -> None:
        path = self._vault_path(name)
        if not path.exists():
            raise VaultNotFoundError(name)
        payload = self._read(path)
        salt = base64.b64decode(payload["salt"])
        fernet = self._make_fernet(password, salt, payload["iterations"])
        self._write(path, salt, payload["iterations"], self._encrypt(fernet, credentials))

    def list(self) -> list[str]:
        return [p.stem for p in VAULTS_DIR.glob("*.vault")]

    def delete(self, name: str) -> None:
        path = self._vault_path(name)
        if not path.exists():
            raise VaultNotFoundError(name)
        path.unlink()

    def export(self, name: str, destination_path: str) -> None:
        shutil.copy(self._vault_path(name), destination_path)

    def import_vault(self, source_path: str) -> str:
        source = Path(source_path)
        try:
            payload = json.loads(source.read_text())
        except Exception:
            raise VaultCorruptError(source_path)
        if not REQUIRED_KEYS.issubset(payload):
            raise VaultCorruptError(source_path)

        dest = VAULTS_DIR / source.name
        if dest.exists():
            stem = source.stem
            i = 2
            while dest.exists():
                dest = VAULTS_DIR / f"{stem}_{i}.vault"
                i += 1

        shutil.copy(source, dest)
        return dest.stem

    @staticmethod
    def new_credential(title="", username="", password="", url="", notes="") -> dict:
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "username": username,
            "password": password,
            "url": url,
            "notes": notes,
        }

    def _vault_path(self, name: str) -> Path:
        return VAULTS_DIR / f"{name}.vault"

    def _make_fernet(self, password: str, salt: bytes, iterations: int = ITERATIONS) -> Fernet:
        kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=iterations)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)

    def _encrypt(self, fernet: Fernet, credentials: list) -> bytes:
        return fernet.encrypt(json.dumps(credentials).encode())

    def _decrypt(self, fernet: Fernet, token: bytes) -> list:
        try:
            plaintext = fernet.decrypt(token)
        except InvalidToken:
            raise VaultWrongPasswordError
        try:
            return json.loads(plaintext)
        except json.JSONDecodeError:
            raise VaultCorruptError

    def _read(self, path: Path) -> dict:
        try:
            payload = json.loads(path.read_text())
        except Exception:
            raise VaultCorruptError(path)
        if not REQUIRED_KEYS.issubset(payload):
            raise VaultCorruptError(path)
        return payload

    def _write(self, path: Path, salt: bytes, iterations: int, token: bytes) -> None:
        payload = {
            "salt": base64.b64encode(salt).decode(),
            "iterations": iterations,
            "data": token.decode(),
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload))
        os.replace(tmp, path)
