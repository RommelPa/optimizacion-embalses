from __future__ import annotations

from datetime import datetime
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
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QScrollArea,
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
            "Revise la corrida seleccionada, sus datos principales, "
            "la configuración usada, las observaciones y la auditoría de ejecución."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        main_layout.addLayout(self._build_top_summary_layout())
        main_layout.addWidget(self._build_contexto_group())
        main_layout.addWidget(self._build_configuracion_group())
        main_layout.addWidget(self._build_error_group())
        main_layout.addLayout(self._build_actions())
        main_layout.addStretch()

    def _create_value_label(self) -> QLabel:
        label = QLabel("-")
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return label

    def _set_label_value(self, label: QLabel, value: str, tooltip: str | None = None) -> None:
        label.setText(value)
        label.setToolTip(tooltip or value)

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

    def _build_contexto_group(self) -> QGroupBox:
        self.contexto_group = QGroupBox("Contexto y auditoría")
        layout = QGridLayout(self.contexto_group)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)

        self.datos_group = QGroupBox("Datos del caso")
        self.datos_form = QFormLayout(self.datos_group)
        self.datos_form.setHorizontalSpacing(20)
        self.datos_form.setVerticalSpacing(12)

        self.escenario_label = self._create_value_label()
        self.observaciones_label = self._create_value_label()

        self.datos_form.addRow("Escenario", self.escenario_label)
        self.datos_form.addRow("Observaciones", self.observaciones_label)

        self.auditoria_group = QGroupBox("Auditoría de ejecución")
        self.auditoria_form = QFormLayout(self.auditoria_group)
        self.auditoria_form.setHorizontalSpacing(20)
        self.auditoria_form.setVerticalSpacing(12)

        self.usuario_label = self._create_value_label()
        self.usuario_rol_label = self._create_value_label()
        self.created_at_label = self._create_value_label()

        self.auditoria_form.addRow("Ejecutada por", self.usuario_label)
        self.auditoria_form.addRow("Rol", self.usuario_rol_label)
        self.auditoria_form.addRow("Fecha de registro", self.created_at_label)

        layout.addWidget(self.datos_group, 0, 0)
        layout.addWidget(self.auditoria_group, 0, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        return self.contexto_group

    def _build_configuracion_group(self) -> QGroupBox:
        self.config_group = QGroupBox("Configuración usada")
        layout = QGridLayout(self.config_group)
        layout.setHorizontalSpacing(24)
        layout.setVerticalSpacing(16)

        self.cfg_algoritmo_group = QGroupBox("PSO")
        self.cfg_algoritmo_form = QFormLayout(self.cfg_algoritmo_group)
        self.cfg_algoritmo_form.setHorizontalSpacing(20)
        self.cfg_algoritmo_form.setVerticalSpacing(10)

        self.cfg_c1_label = self._create_value_label()
        self.cfg_c2_label = self._create_value_label()
        self.cfg_w_label = self._create_value_label()
        self.cfg_v_max_label = self._create_value_label()
        self.cfg_n_particles_label = self._create_value_label()
        self.cfg_max_iter_label = self._create_value_label()

        self.cfg_algoritmo_form.addRow("c1", self.cfg_c1_label)
        self.cfg_algoritmo_form.addRow("c2", self.cfg_c2_label)
        self.cfg_algoritmo_form.addRow("w", self.cfg_w_label)
        self.cfg_algoritmo_form.addRow("v_max", self.cfg_v_max_label)
        self.cfg_algoritmo_form.addRow("N partículas", self.cfg_n_particles_label)
        self.cfg_algoritmo_form.addRow("Max iter", self.cfg_max_iter_label)

        self.cfg_modelo_group = QGroupBox("Modelo")
        self.cfg_modelo_form = QFormLayout(self.cfg_modelo_group)
        self.cfg_modelo_form.setHorizontalSpacing(20)
        self.cfg_modelo_form.setVerticalSpacing(10)

        self.cfg_rend_ch4_label = self._create_value_label()
        self.cfg_rend_ch6_label = self._create_value_label()
        self.cfg_v_inicio_label = self._create_value_label()
        self.cfg_v_final_label = self._create_value_label()

        self.cfg_modelo_form.addRow("Rendimiento CH4", self.cfg_rend_ch4_label)
        self.cfg_modelo_form.addRow("Rendimiento CH6", self.cfg_rend_ch6_label)
        self.cfg_modelo_form.addRow("Factor volumen inicial", self.cfg_v_inicio_label)
        self.cfg_modelo_form.addRow("Factor volumen final", self.cfg_v_final_label)

        self.cfg_restricciones_group = QGroupBox("Restricciones")
        self.cfg_restricciones_form = QFormLayout(self.cfg_restricciones_group)
        self.cfg_restricciones_form.setHorizontalSpacing(20)
        self.cfg_restricciones_form.setVerticalSpacing(10)

        self.cfg_v_cincel_max_label = self._create_value_label()
        self.cfg_v_cincel_min_label = self._create_value_label()
        self.cfg_v_camp_max_label = self._create_value_label()
        self.cfg_v_camp_min_label = self._create_value_label()
        self.cfg_q_min_label = self._create_value_label()
        self.cfg_q_max_label = self._create_value_label()

        self.cfg_restricciones_form.addRow("V Cincel max", self.cfg_v_cincel_max_label)
        self.cfg_restricciones_form.addRow("V Cincel min", self.cfg_v_cincel_min_label)
        self.cfg_restricciones_form.addRow("V Campanario max", self.cfg_v_camp_max_label)
        self.cfg_restricciones_form.addRow("V Campanario min", self.cfg_v_camp_min_label)
        self.cfg_restricciones_form.addRow("Q rango min", self.cfg_q_min_label)
        self.cfg_restricciones_form.addRow("Q rango max", self.cfg_q_max_label)

        layout.addWidget(self.cfg_algoritmo_group, 0, 0)
        layout.addWidget(self.cfg_modelo_group, 0, 1)
        layout.addWidget(self.cfg_restricciones_group, 0, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        return self.config_group

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
        corrida_id_text = str(detail.get("id", "-"))

        self._set_label_value(self.id_label, corrida_id_text, corrida_id_text)
        self._set_label_value(self.caso_estudio_label, self._format_text(detail.get("caso_estudio")))
        self._set_label_value(self.estado_label, self._format_text(detail.get("estado")))
        self._set_label_value(self.origen_label, self._format_text(detail.get("origen_datos")))
        self._set_label_value(self.fecha_label, self._format_text(detail.get("fecha_proceso")))
        self._set_label_value(self.best_cost_label, self._format_number(best_cost, 2))
        self._set_label_value(self.tiempo_label, self._format_number(execution_time, 2))
        self._set_label_value(self.q_salida_label, self._format_number(q_salida, 3))
        self._set_label_value(self.version_modelo_label, self._format_text(detail.get("version_modelo")))
        self._set_label_value(self.modo_ejecucion_label, self._format_text(detail.get("modo_ejecucion")))
        self._set_label_value(self.modo_operacion_label, self._format_text(detail.get("modo_operacion")))

        self._set_label_value(self.escenario_label, self._format_text(detail.get("escenario")))
        self._set_label_value(
            self.observaciones_label,
            self._format_text(detail.get("observaciones"), empty_text="Sin observaciones"),
        )
        self._set_label_value(self.usuario_label, self._format_text(detail.get("usuario_username")))
        self._set_label_value(self.usuario_rol_label, self._format_text(detail.get("usuario_rol")))
        self._set_label_value(
            self.created_at_label,
            self._format_datetime_display(detail.get("created_at")),
            self._format_text(detail.get("created_at")),
        )

        configuracion_usada = detail.get("configuracion_usada", {}) or {}
        self._load_configuracion_usada(configuracion_usada)

        q_opt = detail.get("q_opt", []) or []
        ingreso = detail.get("ingreso", []) or []

        self._set_label_value(self.periodos_label, str(len(q_opt)))
        self._set_label_value(self.q_min_label, self._format_sequence_stat(q_opt, "min", 3))
        self._set_label_value(self.q_max_label, self._format_sequence_stat(q_opt, "max", 3))
        self._set_label_value(self.q_promedio_label, self._format_sequence_stat(q_opt, "avg", 3))
        self._set_label_value(
            self.ingreso_total_label,
            self._format_number(sum(ingreso), 2) if ingreso else "-",
        )

        error_message = detail.get("error_message")
        if error_message:
            self.error_label.setText(str(error_message))
            self.error_label.setToolTip(str(error_message))
            self.error_group.setVisible(True)
        else:
            self.error_label.setText("-")
            self.error_label.setToolTip("")
            self.error_group.setVisible(False)

    def _load_configuracion_usada(self, data: dict) -> None:
        self._set_label_value(self.cfg_c1_label, self._format_number(data.get("c1"), 4))
        self._set_label_value(self.cfg_c2_label, self._format_number(data.get("c2"), 4))
        self._set_label_value(self.cfg_w_label, self._format_number(data.get("w"), 4))
        self._set_label_value(self.cfg_v_max_label, self._format_number(data.get("v_max"), 4))
        self._set_label_value(self.cfg_n_particles_label, self._format_int(data.get("n_particles")))
        self._set_label_value(self.cfg_max_iter_label, self._format_int(data.get("max_iter")))

        self._set_label_value(
            self.cfg_rend_ch4_label,
            self._format_number(data.get("rendimiento_ch4"), 4),
        )
        self._set_label_value(
            self.cfg_rend_ch6_label,
            self._format_number(data.get("rendimiento_ch6"), 4),
        )
        self._set_label_value(
            self.cfg_v_inicio_label,
            self._format_number(data.get("v_inicio_factor"), 4),
        )
        self._set_label_value(
            self.cfg_v_final_label,
            self._format_number(data.get("v_final_factor"), 4),
        )

        self._set_label_value(
            self.cfg_v_cincel_max_label,
            self._format_number(data.get("v_cincel_max"), 2),
        )
        self._set_label_value(
            self.cfg_v_cincel_min_label,
            self._format_number(data.get("v_cincel_min"), 2),
        )
        self._set_label_value(
            self.cfg_v_camp_max_label,
            self._format_number(data.get("v_campanario_max"), 2),
        )
        self._set_label_value(
            self.cfg_v_camp_min_label,
            self._format_number(data.get("v_campanario_min"), 2),
        )
        self._set_label_value(
            self.cfg_q_min_label,
            self._format_number(data.get("q_rango_min"), 4),
        )
        self._set_label_value(
            self.cfg_q_max_label,
            self._format_number(data.get("q_rango_max"), 4),
        )

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

    def _format_text(self, value: object, empty_text: str = "-") -> str:
        if value is None:
            return empty_text

        text = str(value).strip()
        return text if text else empty_text

    def _format_int(self, value: object) -> str:
        if value is None:
            return "-"

        try:
            return str(int(float(str(value))))
        except (ValueError, TypeError):
            return str(value)

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

    def _format_sequence_stat(
        self,
        values: list[float],
        stat: str,
        decimals: int = 3,
    ) -> str:
        if not values:
            return "-"

        if stat == "min":
            return self._format_number(min(values), decimals)
        if stat == "max":
            return self._format_number(max(values), decimals)
        if stat == "avg":
            return self._format_number(sum(values) / len(values), decimals)

        return "-"

    def _format_datetime_display(self, value: object) -> str:
        if value is None:
            return "-"

        text = str(value).strip()
        if not text:
            return "-"

        try:
            iso_text = text.replace("Z", "+00:00")
            dt = datetime.fromisoformat(iso_text)
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return text