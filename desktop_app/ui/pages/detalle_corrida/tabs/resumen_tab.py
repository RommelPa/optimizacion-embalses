from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.pages.detalle_corrida.formatters import (
    format_datetime_display,
    format_number,
    format_sequence_stat,
    format_text,
)


class ResumenTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addLayout(self._build_top_summary_layout())
        layout.addWidget(self._build_contexto_group())
        layout.addWidget(self._build_error_group())
        layout.addStretch()

    def _create_value_label(self) -> QLabel:
        label = QLabel("-")
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return label

    def _set_label_value(
        self,
        label: QLabel,
        value: str,
        tooltip: str | None = None,
    ) -> None:
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

    def _build_error_group(self) -> QGroupBox:
        self.error_group = QGroupBox("Detalle de error")
        error_layout = QVBoxLayout(self.error_group)

        self.error_label = QLabel("-")
        self.error_label.setObjectName("StatusPanel")
        self.error_label.setWordWrap(True)
        self.error_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        error_layout.addWidget(self.error_label)
        self.error_group.setVisible(False)
        return self.error_group

    def set_detail(self, detail: dict) -> None:
        best_cost = detail.get("best_cost")
        execution_time = detail.get("execution_time_sec")
        q_salida = detail.get("q_salida_campanario")
        corrida_id_text = str(detail.get("id", "-"))

        self._set_label_value(self.id_label, corrida_id_text, corrida_id_text)
        self._set_label_value(
            self.caso_estudio_label,
            format_text(detail.get("caso_estudio")),
        )
        self._set_label_value(self.estado_label, format_text(detail.get("estado")))
        self._set_label_value(self.origen_label, format_text(detail.get("origen_datos")))
        self._set_label_value(self.fecha_label, format_text(detail.get("fecha_proceso")))
        self._set_label_value(self.best_cost_label, format_number(best_cost, 2))
        self._set_label_value(self.tiempo_label, format_number(execution_time, 2))
        self._set_label_value(self.q_salida_label, format_number(q_salida, 3))
        self._set_label_value(
            self.version_modelo_label,
            format_text(detail.get("version_modelo")),
        )
        self._set_label_value(
            self.modo_ejecucion_label,
            format_text(detail.get("modo_ejecucion")),
        )
        self._set_label_value(
            self.modo_operacion_label,
            format_text(detail.get("modo_operacion")),
        )

        self._set_label_value(self.escenario_label, format_text(detail.get("escenario")))
        self._set_label_value(
            self.observaciones_label,
            format_text(detail.get("observaciones"), empty_text="Sin observaciones"),
        )
        self._set_label_value(
            self.usuario_label,
            format_text(detail.get("usuario_username")),
        )
        self._set_label_value(
            self.usuario_rol_label,
            format_text(detail.get("usuario_rol")),
        )
        self._set_label_value(
            self.created_at_label,
            format_datetime_display(detail.get("created_at")),
            format_text(detail.get("created_at")),
        )

        q_opt = detail.get("q_opt", []) or []
        ingreso = detail.get("ingreso", []) or []

        self._set_label_value(self.periodos_label, str(len(q_opt)))
        self._set_label_value(self.q_min_label, format_sequence_stat(q_opt, "min", 3))
        self._set_label_value(self.q_max_label, format_sequence_stat(q_opt, "max", 3))
        self._set_label_value(self.q_promedio_label, format_sequence_stat(q_opt, "avg", 3))
        self._set_label_value(
            self.ingreso_total_label,
            format_number(sum(ingreso), 2) if ingreso else "-",
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