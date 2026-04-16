from app.db.base import Base
from app.db.session import engine

# Importa los modelos para que SQLAlchemy los registre
from app.models.corrida import Corrida  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)