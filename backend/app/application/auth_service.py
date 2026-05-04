from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.application.password_service import PasswordService
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


@dataclass
class UsuarioSesion:
    id: int
    username: str
    rol: str


class AuthService:
    MAX_INTENTOS_FALLIDOS = 5
    BLOQUEO_MINUTOS = 10

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = UsuarioRepository(db)
        self.password_service = PasswordService()

    def autenticar(self, username: str, password: str) -> UsuarioSesion:
        username = username.strip()
        if not username or not password:
            raise ValueError("Usuario y contraseña son obligatorios.")

        usuario = self.repo.get_by_username(username)
        if usuario is None:
            raise ValueError("Usuario o contraseña incorrectos.")

        if not usuario.activo:
            raise ValueError("El usuario está inactivo.")

        now = datetime.now(timezone.utc)
        if usuario.bloqueado_hasta is not None:
            bloqueado_hasta = self._ensure_utc(usuario.bloqueado_hasta)
            if bloqueado_hasta > now:
                raise ValueError("Usuario bloqueado temporalmente. Intente más tarde.")

        if not self.password_service.verify_password(password, usuario.password_hash):
            self._registrar_intento_fallido(usuario, now)
            raise ValueError("Usuario o contraseña incorrectos.")

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None
        usuario.ultimo_login_at = now
        self.repo.update(usuario)

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
                password_hash=self.password_service.hash_password(password),
                rol=rol,
                activo=True,
                intentos_fallidos=0,
                bloqueado_hasta=None,
                ultimo_login_at=None,
            )
            self.repo.add(usuario)

    def _registrar_intento_fallido(self, usuario: Usuario, now: datetime) -> None:
        usuario.intentos_fallidos += 1

        if usuario.intentos_fallidos >= self.MAX_INTENTOS_FALLIDOS:
            usuario.bloqueado_hasta = now + timedelta(minutes=self.BLOQUEO_MINUTOS)
            usuario.intentos_fallidos = 0

        self.repo.update(usuario)

    def _ensure_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)