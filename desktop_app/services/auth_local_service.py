from __future__ import annotations

from app.application.auth_service import AuthService, UsuarioSesion
from app.db.session import SessionLocal


class AuthLocalService:
    def autenticar(self, username: str, password: str) -> UsuarioSesion:
        db = SessionLocal()
        try:
            service = AuthService(db)
            return service.autenticar(username, password)
        finally:
            db.close()