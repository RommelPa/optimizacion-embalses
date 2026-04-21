from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from services.corrida_local_service import CorridaLocalService


class DetalleCorridaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.current_corrida_id: str | None = None
        self.current_caso_estudio: str | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Detalle de corrida")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)

        self.meta_group = QGroupBox("Resumen")
        self.meta_form = QFormLayout(self.meta_group)

        self.id_label = QLabel("-")
        self.caso_estudio_label = QLabel("-")
        self.estado_label = QLabel("-")
        self.origen_label = QLabel("-")
        self.fecha_label = QLabel("-")
        self.best_cost_label = QLabel("-")
        self.tiempo_label = QLabel("-")
        self.q_salida_label = QLabel("-")
        self.version_modelo_label = QLabel("-")
        self.modo_ejecucion_label = QLabel("-")
        self.modo_operacion_label = QLabel("-")

        self.meta_form.addRow("ID", self.id_label)
        self.meta_form.addRow("Caso de estudio", self.caso_estudio_label)
        self.meta_form.addRow("Estado", self.estado_label)
        self.meta_form.addRow("Origen de datos", self.origen_label)
        self.meta_form.addRow("Fecha de proceso", self.fecha_label)
        self.meta_form.addRow("Mejor costo", self.best_cost_label)
        self.meta_form.addRow("Tiempo de ejecución (s)", self.tiempo_label)
        self.meta_form.addRow("Q salida Campanario", self.q_salida_label)
        self.meta_form.addRow("Versión del modelo", self.version_modelo_label)
        self.meta_form.addRow("Modo de ejecución", self.modo_ejecucion_label)
        self.meta_form.addRow("Modo de operación", self.modo_operacion_label)

        layout.addWidget(self.meta_group)

        self.operativo_group = QGroupBox("Resumen operativo")
        self.operativo_form = QFormLayout(self.operativo_group)

        self.periodos_label = QLabel("-")
        self.q_min_label = QLabel("-")
        self.q_max_label = QLabel("-")
        self.q_promedio_label = QLabel("-")
        self.ingreso_total_label = QLabel("-")

        self.operativo_form.addRow("Períodos", self.periodos_label)
        self.operativo_form.addRow("Q mínima", self.q_min_label)
        self.operativo_form.addRow("Q máxima", self.q_max_label)
        self.operativo_form.addRow("Q promedio", self.q_promedio_label)
        self.operativo_form.addRow("Ingreso total estimado", self.ingreso_total_label)

        layout.addWidget(self.operativo_group)

        self.mensaje_group = QGroupBox("Mensaje del modelo")
        self.mensaje_layout = QVBoxLayout(self.mensaje_group)
        self.mensaje_label = QLabel("-")
        self.mensaje_label.setWordWrap(True)
        self.mensaje_layout.addWidget(self.mensaje_label)
        layout.addWidget(self.mensaje_group)

        self.error_group = QGroupBox("Detalle de error")
        self.error_layout = QVBoxLayout(self.error_group)
        self.error_label = QLabel("-")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #d9534f;")
        self.error_layout.addWidget(self.error_label)
        layout.addWidget(self.error_group)
        self.error_group.setVisible(False)

        self.payload_group = QGroupBox("Payload de entrada")
        self.payload_layout = QVBoxLayout(self.payload_group)
        self.payload_text = QTextEdit()
        self.payload_text.setReadOnly(True)
        self.payload_text.setPlaceholderText("Aquí se mostrará el payload de entrada.")
        self.payload_layout.addWidget(self.payload_text)
        layout.addWidget(self.payload_group)

        self.export_btn = QPushButton("Exportar Excel")
        self.export_btn.clicked.connect(self.export_excel)
        layout.addWidget(self.export_btn)

        layout.addStretch()

    def load_corrida(self, corrida_id: str) -> None:
        detail = self.service.obtener_corrida(corrida_id)
        self.current_corrida_id = corrida_id
        self.current_caso_estudio = detail.get("caso_estudio", "")

        self.id_label.setText(detail.get("id", "-"))
        self.caso_estudio_label.setText(detail.get("caso_estudio", "-"))
        self.estado_label.setText(detail.get("estado", "-"))
        self.origen_label.setText(detail.get("origen_datos", "-"))
        self.fecha_label.setText(detail.get("fecha_proceso", "-"))
        self.best_cost_label.setText(str(detail.get("best_cost", "-")))
        self.tiempo_label.setText(str(detail.get("execution_time_sec", "-")))
        self.q_salida_label.setText(str(detail.get("q_salida_campanario", "-")))
        self.version_modelo_label.setText(detail.get("version_modelo", "-"))
        self.modo_ejecucion_label.setText(detail.get("modo_ejecucion", "-"))
        self.modo_operacion_label.setText(detail.get("modo_operacion", "-"))
        self.payload_text.setText(detail.get("input_payload_json", ""))

        q_opt = detail.get("q_opt", []) or []
        ingreso = detail.get("ingreso", []) or []

        self.periodos_label.setText(str(len(q_opt)))
        self.q_min_label.setText(f"{min(q_opt):.3f}" if q_opt else "-")
        self.q_max_label.setText(f"{max(q_opt):.3f}" if q_opt else "-")
        self.q_promedio_label.setText(
            f"{(sum(q_opt) / len(q_opt)):.3f}" if q_opt else "-"
        )
        self.ingreso_total_label.setText(
            f"{sum(ingreso):.2f}" if ingreso else "-"
        )

        estado = detail.get("estado", "-")
        modo_ejecucion = detail.get("modo_ejecucion", "-")
        mensaje_modelo = detail.get("mensaje_modelo", "-")
        error_message = detail.get("error_message")

        mensaje_estado, mostrar_error = self._build_estado_descripcion(
            estado=estado,
            modo_ejecucion=modo_ejecucion,
            mensaje_modelo=mensaje_modelo,
            error_message=error_message,
        )

        self.mensaje_label.setText(mensaje_estado)

        if mostrar_error:
            self.error_label.setText(error_message or mensaje_estado)
            self.error_group.setVisible(True)
        else:
            self.error_label.setText("-")
            self.error_group.setVisible(False)

    def export_excel(self) -> None:
        if not self.current_corrida_id:
            QMessageBox.warning(self, "Validación", "No hay corrida cargada.")
            return

        caso = (self.current_caso_estudio or "corrida").strip()
        caso_sanitizado = "".join(
            ch if ch.isalnum() or ch in ("-", "_") else "_"
            for ch in caso
        ).strip("_")
        caso_sanitizado = caso_sanitizado[:40] or "corrida"
        sugerido = f"{caso_sanitizado}_{self.current_corrida_id[:8]}.xlsx"

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            sugerido,
            "Excel (*.xlsx)",
        )
        if not filepath:
            return

        try:
            self.service.descargar_excel(self.current_corrida_id, Path(filepath))
            QMessageBox.information(self, "Éxito", "Excel exportado correctamente.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el Excel:\n{exc}")

    def _build_estado_descripcion(
        self,
        estado: str,
        modo_ejecucion: str,
        mensaje_modelo: str,
        error_message: str | None,
    ) -> tuple[str, bool]:
        estado_normalizado = (estado or "").strip().lower()
        modo_normalizado = (modo_ejecucion or "").strip().lower()

        if estado_normalizado == "completada":
            return mensaje_modelo or "Corrida completada correctamente.", False

        if estado_normalizado == "rechazada":
            if error_message:
                return (
                    "La corrida fue rechazada por validación de entrada.\n\n"
                    f"Detalle: {error_message}",
                    True,
                )
            return (
                "La corrida fue rechazada por validación de entrada.",
                True,
            )

        if estado_normalizado == "fallida":
            if modo_normalizado == "error_ejecucion" and error_message:
                return (
                    "La corrida falló durante la ejecución del motor.\n\n"
                    f"Detalle: {error_message}",
                    True,
                )
            if error_message:
                return (
                    "La corrida falló por un error no recuperable.\n\n"
                    f"Detalle: {error_message}",
                    True,
                )
            return (
                "La corrida falló por un error no recuperable.",
                True,
            )

        if error_message:
            return (
                f"{mensaje_modelo or 'Estado no reconocido.'}\n\nDetalle: {error_message}",
                True,
            )

        return mensaje_modelo or "Sin información adicional.", False