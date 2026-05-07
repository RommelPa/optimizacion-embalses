from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from services.corrida_local_service import CorridaLocalService


class CorridaManualWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(
        self,
        *,
        caso_estudio: str,
        modo_operacion: str,
        fecha_proceso: str,
        escenario: str,
        origen_datos: str,
        usuario_id: int,
        usuario_username: str,
        usuario_rol: str,
        q_salida_campanario: float,
        cmg: list[float],
        p_char_5: list[float],
        observaciones: str | None = None,
        corrida_base_id: str | None = None,
    ) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.caso_estudio = caso_estudio
        self.modo_operacion = modo_operacion
        self.fecha_proceso = fecha_proceso
        self.escenario = escenario
        self.origen_datos = origen_datos
        self.usuario_id = usuario_id
        self.usuario_username = usuario_username
        self.usuario_rol = usuario_rol
        self.q_salida_campanario = q_salida_campanario
        self.cmg = cmg
        self.p_char_5 = p_char_5
        self.observaciones = observaciones
        self.corrida_base_id = corrida_base_id

    def run(self) -> None:
        try:
            result = self.service.crear_corrida_manual(
                caso_estudio=self.caso_estudio,
                modo_operacion=self.modo_operacion,
                fecha_proceso=self.fecha_proceso,
                escenario=self.escenario,
                origen_datos=self.origen_datos,
                usuario_id=self.usuario_id,
                usuario_username=self.usuario_username,
                usuario_rol=self.usuario_rol,
                q_salida_campanario=self.q_salida_campanario,
                cmg=self.cmg,
                p_char_5=self.p_char_5,
                observaciones=self.observaciones,
                corrida_base_id=self.corrida_base_id,
            )
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))