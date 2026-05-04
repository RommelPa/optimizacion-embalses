from __future__ import annotations


def is_ingeniero(user_session) -> bool:
    rol = getattr(user_session, "rol", "")
    return str(rol).strip().lower() == "ingeniero"


def require_ingeniero(user_session) -> None:
    if not is_ingeniero(user_session):
        raise PermissionError("No tienes permisos para realizar esta acción.")