from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.corrida import Corrida


class CorridaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, corrida: Corrida) -> None:
        self.db.add(corrida)
        self.db.commit()

    def get_by_id(self, corrida_id: str) -> Corrida | None:
        return self.db.query(Corrida).filter(Corrida.id == corrida_id).first()

    def list_all(self) -> list[Corrida]:
        return self.db.query(Corrida).order_by(Corrida.created_at.desc()).all()

    def list_filtered(
        self,
        origen_datos: str | None = None,
        estado: str | None = None,
        id_contains: str | None = None,
        fecha_proceso: str | None = None,
    ) -> list[Corrida]:
        query = self.db.query(Corrida)

        if origen_datos:
            query = query.filter(Corrida.origen_datos == origen_datos)

        if estado:
            query = query.filter(Corrida.estado == estado)

        if fecha_proceso:
            query = query.filter(Corrida.fecha_proceso == fecha_proceso)

        if id_contains:
            query = query.filter(Corrida.id.contains(id_contains))

        return query.order_by(Corrida.created_at.desc()).all()