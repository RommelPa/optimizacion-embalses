from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from services.corrida_local_service import CorridaLocalService


class CorridaWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(
        self,
        caso_estudio: str,
        modo_operacion: str,
        fecha_proceso: str,
        escenario: str,
        origen_datos: str,
        observaciones: str | None,
        archivo_entrada: str | None,
    ) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.caso_estudio = caso_estudio
        self.modo_operacion = modo_operacion
        self.fecha_proceso = fecha_proceso
        self.escenario = escenario
        self.origen_datos = origen_datos
        self.observaciones = observaciones
        self.archivo_entrada = archivo_entrada

    def run(self) -> None:
        try:
            result = self.service.crear_corrida(
                caso_estudio=self.caso_estudio,
                modo_operacion=self.modo_operacion,
                fecha_proceso=self.fecha_proceso,
                escenario=self.escenario,
                origen_datos=self.origen_datos,
                observaciones=self.observaciones,
                archivo_entrada=self.archivo_entrada,
            )
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))