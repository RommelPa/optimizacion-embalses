from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
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
    caso_estudio: Mapped[str] = mapped_column(String, nullable=False, index=True)
    fecha_proceso: Mapped[str] = mapped_column(String, nullable=False)
    modo_operacion: Mapped[str] = mapped_column(String, nullable=False)
    escenario: Mapped[str] = mapped_column(String, nullable=False)
    origen_datos: Mapped[str] = mapped_column(String, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    usuario_username: Mapped[str] = mapped_column(String, nullable=False, index=True, default="")
    usuario_rol: Mapped[str] = mapped_column(String, nullable=False, index=True, default="")

    estado: Mapped[str] = mapped_column(String, nullable=False)
    version_modelo: Mapped[str] = mapped_column(String, nullable=False)
    modo_ejecucion: Mapped[str] = mapped_column(String, nullable=False)
    mensaje_modelo: Mapped[str] = mapped_column(Text, nullable=False)

    best_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    execution_time_sec: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    q_salida_campanario: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    q_opt_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    v_cincel_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    v_campanario_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    cmg_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    potencia_ch4_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    potencia_ch6_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    ingreso_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    p_char_5_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    input_payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    cfg_c1: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    cfg_c2: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    cfg_w: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    cfg_v_max: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    cfg_n_particles: Mapped[int] = mapped_column(Integer, nullable=False, default=150)
    cfg_max_iter: Mapped[int] = mapped_column(Integer, nullable=False, default=150)

    cfg_rendimiento_ch4: Mapped[float] = mapped_column(Float, nullable=False, default=1.01)
    cfg_rendimiento_ch6: Mapped[float] = mapped_column(Float, nullable=False, default=0.59)
    cfg_v_inicio_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    cfg_v_final_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)

    cfg_v_cincel_max: Mapped[float] = mapped_column(Float, nullable=False, default=190000.0)
    cfg_v_cincel_min: Mapped[float] = mapped_column(Float, nullable=False, default=20000.0)
    cfg_v_campanario_max: Mapped[float] = mapped_column(Float, nullable=False, default=90000.0)
    cfg_v_campanario_min: Mapped[float] = mapped_column(Float, nullable=False, default=20000.0)
    cfg_q_rango_min: Mapped[float] = mapped_column(Float, nullable=False, default=6.0)
    cfg_q_rango_max: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)