from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ConfiguracionGlobal(Base):
    __tablename__ = "configuracion_global"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)

    c1: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    c2: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    w: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    v_max: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    n_particles: Mapped[int] = mapped_column(Integer, nullable=False, default=150)
    max_iter: Mapped[int] = mapped_column(Integer, nullable=False, default=150)

    rendimiento_ch4: Mapped[float] = mapped_column(Float, nullable=False, default=1.01)
    rendimiento_ch6: Mapped[float] = mapped_column(Float, nullable=False, default=0.59)
    v_inicio_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    v_final_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)

    v_cincel_max: Mapped[float] = mapped_column(Float, nullable=False, default=190000.0)
    v_cincel_min: Mapped[float] = mapped_column(Float, nullable=False, default=20000.0)
    v_campanario_max: Mapped[float] = mapped_column(Float, nullable=False, default=90000.0)
    v_campanario_min: Mapped[float] = mapped_column(Float, nullable=False, default=20000.0)
    q_rango_min: Mapped[float] = mapped_column(Float, nullable=False, default=6.0)
    q_rango_max: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )