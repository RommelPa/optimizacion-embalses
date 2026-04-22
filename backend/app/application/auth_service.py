from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


@dataclass
class UsuarioSesion:
    id: int
    username: str
    rol: str


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = UsuarioRepository(db)

    def autenticar(self, username: str, password: str) -> UsuarioSesion:
        username = username.strip()
        if not username or not password:
            raise ValueError("Usuario y contraseña son obligatorios.")

        usuario = self.repo.get_by_username(username)
        if usuario is None:
            raise ValueError("Usuario o contraseña incorrectos.")

        if not usuario.activo:
            raise ValueError("El usuario está inactivo.")

        if not self._verify_password(password, usuario.password_hash):
            raise ValueError("Usuario o contraseña incorrectos.")

        return UsuarioSesion(
            id=usuario.id,
            username=usuario.username,
            rol=usuario.rol,
        )

    def ensure_default_users(self) -> None:
        usuarios_base = [
            ("operador", "operador123", "operador"),
            ("ingeniero", "ingeniero123", "ingeniero"),
        ]

        for username, password, rol in usuarios_base:
            existente = self.repo.get_by_username(username)
            if existente is not None:
                continue

            usuario = Usuario(
                username=username,
                password_hash=self._hash_password(password),
                rol=rol,
                activo=True,
            )
            self.repo.add(usuario)

    def _hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        iterations = 120_000
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )
        return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            algorithm, iterations_str, salt_hex, digest_hex = stored_hash.split("$", 3)
            if algorithm != "pbkdf2_sha256":
                return False

            iterations = int(iterations_str)
            salt = bytes.fromhex(salt_hex)
            expected_digest = bytes.fromhex(digest_hex)

            candidate_digest = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations,
            )
            return hmac.compare_digest(candidate_digest, expected_digest)
        except Exception:
            return False