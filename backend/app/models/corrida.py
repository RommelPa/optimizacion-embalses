from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Corrida(Base):
    __tablename__ = "corridas"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

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
    v_cincel_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    v_campanario_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    cmg_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    potencia_ch4_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    potencia_ch6_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    ingreso_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    input_payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)