from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QScrollArea,
)

from services.corrida_local_service import CorridaLocalService
import json

class DetalleCorridaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.current_corrida_id: str | None = None
        self.current_caso_estudio: str | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        root_layout.addWidget(self.scroll_area)

        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        main_layout = QVBoxLayout(self.content_widget)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        title = QLabel("Detalle de corrida")
        title.setObjectName("PageTitle")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "Revise la corrida seleccionada, sus métricas principales, "
            "el mensaje del modelo y el payload de entrada."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        main_layout.addLayout(self._build_top_summary_layout())
        main_layout.addWidget(self._build_mensaje_group())
        main_layout.addWidget(self._build_error_group())
        main_layout.addWidget(self._build_payload_group())
        font = self.payload_text.font()
        font.setFamily("Consolas")
        self.payload_text.setFont(font)
        main_layout.addLayout(self._build_actions())
        main_layout.addStretch()

    def _create_value_label(self) -> QLabel:
        label = QLabel("-")
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return label

    def _build_top_summary_layout(self) -> QGridLayout:
        layout = QGridLayout()
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)

        self.meta_group = QGroupBox("Resumen general")
        self.meta_form = QFormLayout(self.meta_group)
        self.meta_form.setHorizontalSpacing(20)
        self.meta_form.setVerticalSpacing(12)
        self.meta_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        self.meta_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.id_label = self._create_value_label()
        self.caso_estudio_label = self._create_value_label()
        self.estado_label = self._create_value_label()
        self.origen_label = self._create_value_label()
        self.fecha_label = self._create_value_label()
        self.best_cost_label = self._create_value_label()
        self.tiempo_label = self._create_value_label()
        self.q_salida_label = self._create_value_label()
        self.version_modelo_label = self._create_value_label()
        self.modo_ejecucion_label = self._create_value_label()
        self.modo_operacion_label = self._create_value_label()

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

        self.operativo_group = QGroupBox("Resumen operativo")
        self.operativo_form = QFormLayout(self.operativo_group)
        self.operativo_form.setHorizontalSpacing(20)
        self.operativo_form.setVerticalSpacing(12)
        self.operativo_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        self.operativo_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.periodos_label = self._create_value_label()
        self.q_min_label = self._create_value_label()
        self.q_max_label = self._create_value_label()
        self.q_promedio_label = self._create_value_label()
        self.ingreso_total_label = self._create_value_label()

        self.operativo_form.addRow("Períodos", self.periodos_label)
        self.operativo_form.addRow("Q mínima", self.q_min_label)
        self.operativo_form.addRow("Q máxima", self.q_max_label)
        self.operativo_form.addRow("Q promedio", self.q_promedio_label)
        self.operativo_form.addRow("Ingreso total estimado", self.ingreso_total_label)

        layout.addWidget(self.meta_group, 0, 0)
        layout.addWidget(self.operativo_group, 0, 1)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)

        return layout

    def _build_mensaje_group(self) -> QGroupBox:
        self.mensaje_group = QGroupBox("Mensaje del modelo")
        self.mensaje_layout = QVBoxLayout(self.mensaje_group)

        self.mensaje_label = QLabel("-")
        self.mensaje_label.setObjectName("StatusPanel")
        self.mensaje_label.setWordWrap(True)
        self.mensaje_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.mensaje_layout.addWidget(self.mensaje_label)
        return self.mensaje_group

    def _build_error_group(self) -> QGroupBox:
        self.error_group = QGroupBox("Detalle de error")
        self.error_layout = QVBoxLayout(self.error_group)

        self.error_label = QLabel("-")
        self.error_label.setObjectName("StatusPanel")
        self.error_label.setWordWrap(True)
        self.error_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.error_layout.addWidget(self.error_label)
        self.error_group.setVisible(False)
        return self.error_group

    def _build_payload_group(self) -> QGroupBox:
        self.payload_group = QGroupBox("Payload de entrada")
        self.payload_layout = QVBoxLayout(self.payload_group)

        self.payload_text = QTextEdit()
        self.payload_text.setReadOnly(True)
        self.payload_text.setPlaceholderText("Aquí se mostrará el payload de entrada.")
        self.payload_text.setMinimumHeight(220)
        self.payload_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self.payload_layout.addWidget(self.payload_text)
        return self.payload_group

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addStretch()

        self.export_btn = QPushButton("Exportar Excel")
        self.export_btn.setMinimumHeight(34)
        self.export_btn.clicked.connect(self.export_excel)

        actions.addWidget(self.export_btn)
        return actions

    def load_corrida(self, corrida_id: str) -> None:
        detail = self.service.obtener_corrida(corrida_id)
        self.current_corrida_id = corrida_id
        self.current_caso_estudio = detail.get("caso_estudio", "")

        best_cost = detail.get("best_cost")
        execution_time = detail.get("execution_time_sec")
        q_salida = detail.get("q_salida_campanario")

        self.id_label.setText(detail.get("id", "-"))
        self.caso_estudio_label.setText(detail.get("caso_estudio", "-"))
        self.estado_label.setText(detail.get("estado", "-"))
        self.origen_label.setText(detail.get("origen_datos", "-"))
        self.fecha_label.setText(detail.get("fecha_proceso", "-"))
        self.best_cost_label.setText(self._format_number(best_cost, 2))
        self.tiempo_label.setText(self._format_number(execution_time, 4))
        self.q_salida_label.setText(self._format_number(q_salida, 3))
        self.version_modelo_label.setText(detail.get("version_modelo", "-"))
        self.modo_ejecucion_label.setText(detail.get("modo_ejecucion", "-"))
        self.modo_operacion_label.setText(detail.get("modo_operacion", "-"))
        raw_payload = detail.get("input_payload_json", "")
        self.payload_text.setPlainText(self._format_payload_json(raw_payload))

        q_opt = detail.get("q_opt", []) or []
        ingreso = detail.get("ingreso", []) or []

        self.periodos_label.setText(str(len(q_opt)))
        self.q_min_label.setText(f"{min(q_opt):.3f}" if q_opt else "-")
        self.q_max_label.setText(f"{max(q_opt):.3f}" if q_opt else "-")
        self.q_promedio_label.setText(
            f"{(sum(q_opt) / len(q_opt)):.3f}" if q_opt else "-"
        )
        self.ingreso_total_label.setText(
            f"{sum(ingreso):,.2f}" if ingreso else "-"
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
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo exportar el Excel:\n{exc}",
            )

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

    def _format_number(
        self,
        value: float | int | str | None,
        decimals: int = 2,
    ) -> str:
        if value is None:
            return "-"

        try:
            return f"{float(value):,.{decimals}f}"
        except (ValueError, TypeError):
            return str(value)
        
    def _format_payload_json(self, payload: str) -> str:
        if not payload.strip():
            return ""

        try:
            parsed = json.loads(payload)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, TypeError):
            return payload