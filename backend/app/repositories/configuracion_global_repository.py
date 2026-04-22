from sqlalchemy.orm import Session

from app.models.configuracion_global import ConfiguracionGlobal


class ConfiguracionGlobalRepository:
    DEFAULT_ID = 1

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self) -> ConfiguracionGlobal | None:
        return (
            self.db.query(ConfiguracionGlobal)
            .filter(ConfiguracionGlobal.id == self.DEFAULT_ID)
            .first()
        )

    def ensure_exists(self) -> ConfiguracionGlobal:
        row = self.get()
        if row is not None:
            return row

        row = ConfiguracionGlobal(id=self.DEFAULT_ID)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def save(self, row: ConfiguracionGlobal) -> ConfiguracionGlobal:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row