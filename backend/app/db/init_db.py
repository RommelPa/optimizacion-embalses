from app.db.base import Base
from app.db.session import engine, SessionLocal

from app.application.auth_service import AuthService
from app.models.configuracion_global import ConfiguracionGlobal  # noqa: F401
from app.models.corrida import Corrida  # noqa: F401
from app.models.usuario import Usuario  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        auth_service.ensure_default_users()
    finally:
        db.close()