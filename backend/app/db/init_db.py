from app.db.base import Base
from app.db.session import engine

from app.models.configuracion_global import ConfiguracionGlobal  # noqa: F401
from app.models.corrida import Corrida  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)