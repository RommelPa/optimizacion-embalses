import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


APP_DIR_NAME = "OptimizacionEmbalses"


def _get_default_sqlite_path() -> Path:
    local_appdata = os.getenv("LOCALAPPDATA")

    if local_appdata:
        base_dir = Path(local_appdata) / APP_DIR_NAME
    else:
        base_dir = Path.home() / f".{APP_DIR_NAME.lower()}"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "corridas.db"


DEFAULT_SQLITE_PATH = _get_default_sqlite_path()
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)