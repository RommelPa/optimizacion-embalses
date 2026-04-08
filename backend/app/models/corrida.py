from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Corrida(Base):
    __tablename__ = "corridas"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    fecha_proceso: Mapped[str] = mapped_column(String, nullable=False)
    modo_operacion: Mapped[str] = mapped_column(String, nullable=False)
    escenario: Mapped[str] = mapped_column(String, nullable=False)
    origen_datos: Mapped[str] = mapped_column(String, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    estado: Mapped[str] = mapped_column(String, nullable=False)
    version_modelo: Mapped[str] = mapped_column(String, nullable=False)
    modo_ejecucion: Mapped[str] = mapped_column(String, nullable=False)
    mensaje_modelo: Mapped[str] = mapped_column(Text, nullable=False)

    best_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    execution_time_sec: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    q_opt_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    input_payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)