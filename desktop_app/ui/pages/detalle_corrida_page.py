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

        self.meta_form.addRow("ID", self.id_label)
        self.meta_form.addRow("Caso de estudio", self.caso_estudio_label)
        self.meta_form.addRow("Estado", self.estado_label)
        self.meta_form.addRow("Origen", self.origen_label)
        self.meta_form.addRow("Fecha proceso", self.fecha_label)
        self.meta_form.addRow("Best cost", self.best_cost_label)
        self.meta_form.addRow("Tiempo ejecución", self.tiempo_label)
        self.meta_form.addRow("Q salida campanario", self.q_salida_label)
        self.meta_form.addRow("Versión modelo", self.version_modelo_label)
        self.meta_form.addRow("Modo ejecución", self.modo_ejecucion_label)

        layout.addWidget(self.meta_group)

        self.mensaje_group = QGroupBox("Mensaje del modelo")
        self.mensaje_layout = QVBoxLayout(self.mensaje_group)
        self.mensaje_label = QLabel("-")
        self.mensaje_label.setWordWrap(True)
        self.mensaje_layout.addWidget(self.mensaje_label)
        layout.addWidget(self.mensaje_group)

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
        self.mensaje_label.setText(detail.get("mensaje_modelo", "-"))
        self.payload_text.setText(detail.get("input_payload_json", ""))

    def export_excel(self) -> None:
        if not self.current_corrida_id:
            QMessageBox.warning(self, "Validación", "No hay corrida cargada.")
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            f"{self.current_corrida_id}.xlsx",
            "Excel (*.xlsx)",
        )
        if not filepath:
            return

        try:
            self.service.descargar_excel(self.current_corrida_id, Path(filepath))
            QMessageBox.information(self, "Éxito", "Excel exportado correctamente.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el Excel:\n{exc}")