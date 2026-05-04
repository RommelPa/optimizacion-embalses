from __future__ import annotations

from app.application.usuario_service import UsuarioService
from app.db.session import SessionLocal


class UsuarioLocalService:
    def listar_usuarios(self, user_session) -> list[dict]:
        db = SessionLocal()
        try:
            service = UsuarioService(db)
            return service.listar_usuarios(user_session)
        finally:
            db.close()

    def crear_usuario(
        self,
        user_session,
        username: str,
        password: str,
        rol: str,
    ) -> dict:
        db = SessionLocal()
        try:
            service = UsuarioService(db)
            return service.crear_usuario(user_session, username, password, rol)
        finally:
            db.close()

    def cambiar_rol(
        self,
        user_session,
        usuario_id: int,
        nuevo_rol: str,
    ) -> dict:
        db = SessionLocal()
        try:
            service = UsuarioService(db)
            return service.cambiar_rol(user_session, usuario_id, nuevo_rol)
        finally:
            db.close()

    def cambiar_estado(
        self,
        user_session,
        usuario_id: int,
        activo: bool,
    ) -> dict:
        db = SessionLocal()
        try:
            service = UsuarioService(db)
            return service.cambiar_estado(user_session, usuario_id, activo)
        finally:
            db.close()

    def resetear_password(
        self,
        user_session,
        usuario_id: int,
        nueva_password: str,
    ) -> dict:
        db = SessionLocal()
        try:
            service = UsuarioService(db)
            return service.resetear_password(user_session, usuario_id, nueva_password)
        finally:
            db.close()