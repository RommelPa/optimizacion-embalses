from __future__ import annotations

import re

from app.application.authorization import require_ingeniero
from app.application.password_service import PasswordService
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    ROLES_VALIDOS = {"operador", "ingeniero"}
    USERNAME_PATTERN = re.compile(r"[a-z0-9._-]{3,30}")

    def __init__(self, db) -> None:
        self.db = db
        self.repo = UsuarioRepository(db)
        self.password_service = PasswordService()

    def listar_usuarios(self, user_session) -> list[dict]:
        require_ingeniero(user_session)

        usuarios = self.repo.list_all()
        return [
            {
                "id": usuario.id,
                "username": usuario.username,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at,
                "updated_at": usuario.updated_at,
                "ultimo_login_at": usuario.ultimo_login_at,
            }
            for usuario in usuarios
        ]

    def crear_usuario(
        self,
        user_session,
        username: str,
        password: str,
        rol: str,
    ) -> dict:
        require_ingeniero(user_session)

        username = username.strip().lower()
        rol = rol.strip().lower()

        if not username:
            raise ValueError("El usuario es obligatorio.")

        if not self.USERNAME_PATTERN.fullmatch(username):
            raise ValueError(
                "El usuario debe tener entre 3 y 30 caracteres y solo puede contener letras, números, punto, guion y guion bajo."
            )

        if not password.strip():
            raise ValueError("La contraseña es obligatoria.")

        if rol not in self.ROLES_VALIDOS:
            raise ValueError("El rol es inválido.")

        if self.repo.exists_by_username(username):
            raise ValueError("Ya existe un usuario con ese nombre.")

        usuario = Usuario(
            username=username,
            password_hash=self.password_service.hash_password(password),
            rol=rol,
            activo=True,
            intentos_fallidos=0,
            bloqueado_hasta=None,
            ultimo_login_at=None,
        )
        usuario = self.repo.add(usuario)

        return self._build_usuario_output(usuario)

    def cambiar_rol(
        self,
        user_session,
        usuario_id: int,
        nuevo_rol: str,
    ) -> dict:
        require_ingeniero(user_session)

        nuevo_rol = nuevo_rol.strip().lower()
        if nuevo_rol not in self.ROLES_VALIDOS:
            raise ValueError("El rol es inválido.")

        usuario = self.repo.get_by_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuario no encontrado.")

        if (
            usuario.rol == "ingeniero"
            and nuevo_rol != "ingeniero"
            and usuario.activo
            and self.repo.count_active_ingenieros() <= 1
        ):
            raise ValueError("No puedes degradar al último ingeniero activo.")

        usuario.rol = nuevo_rol
        usuario = self.repo.update(usuario)
        return self._build_usuario_output(usuario)

    def cambiar_estado(
        self,
        user_session,
        usuario_id: int,
        activo: bool,
    ) -> dict:
        require_ingeniero(user_session)

        usuario = self.repo.get_by_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuario no encontrado.")

        if (
            usuario.rol == "ingeniero"
            and usuario.activo
            and not activo
            and self.repo.count_active_ingenieros() <= 1
        ):
            raise ValueError("No puedes inactivar al último ingeniero activo.")

        usuario.activo = activo
        usuario = self.repo.update(usuario)
        return self._build_usuario_output(usuario)

    def resetear_password(
        self,
        user_session,
        usuario_id: int,
        nueva_password: str,
    ) -> dict:
        require_ingeniero(user_session)

        if not nueva_password.strip():
            raise ValueError("La nueva contraseña es obligatoria.")

        usuario = self.repo.get_by_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuario no encontrado.")

        usuario.password_hash = self.password_service.hash_password(nueva_password)
        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None

        usuario = self.repo.update(usuario)
        return self._build_usuario_output(usuario)

    def _build_usuario_output(self, usuario: Usuario) -> dict:
        return {
            "id": usuario.id,
            "username": usuario.username,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "created_at": usuario.created_at,
            "updated_at": usuario.updated_at,
            "ultimo_login_at": usuario.ultimo_login_at,
        }