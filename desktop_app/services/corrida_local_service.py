from __future__ import annotations

from pathlib import Path
from typing import Any

from app.application.corrida_service import CorridaService
from app.application.dto import CrearCorridaInput
from app.db.session import SessionLocal


class CorridaLocalService:
    def crear_corrida(
        self,
        caso_estudio: str,
        modo_operacion: str,
        fecha_proceso: str,
        escenario: str,
        origen_datos: str,
        usuario_id: int,
        usuario_username: str,
        usuario_rol: str,
        observaciones: str | None,
        archivo_entrada: str | None,
    ) -> dict[str, Any]:
        db = SessionLocal()
        try:
            service = CorridaService(db)
            return service.crear_corrida(
                CrearCorridaInput(
                    caso_estudio=caso_estudio,
                    modo_operacion=modo_operacion,
                    fecha_proceso=fecha_proceso,
                    escenario=escenario,
                    origen_datos=origen_datos,
                    usuario_id=usuario_id,
                    usuario_username=usuario_username,
                    usuario_rol=usuario_rol,
                    observaciones=observaciones,
                    archivo_entrada=archivo_entrada,
                )
            )
        finally:
            db.close()

    def listar_corridas(self) -> dict[str, Any]:
        db = SessionLocal()
        try:
            service = CorridaService(db)
            return service.listar_corridas()
        finally:
            db.close()

    def obtener_corrida(self, corrida_id: str) -> dict[str, Any]:
        db = SessionLocal()
        try:
            service = CorridaService(db)
            return service.obtener_corrida(corrida_id)
        finally:
            db.close()

    def descargar_excel(self, corrida_id: str, output_path: str | Path) -> Path:
        db = SessionLocal()
        try:
            service = CorridaService(db)
            content, _filename = service.exportar_corrida_excel(corrida_id)
            output_path = Path(output_path)
            output_path.write_bytes(content)
            return output_path
        finally:
            db.close()