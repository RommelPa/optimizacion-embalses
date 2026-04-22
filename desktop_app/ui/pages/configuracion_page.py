from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ConfiguracionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
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

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Configuración")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Esta pantalla prepara la configuración global del sistema. "
            "La edición operativa se habilitará en una versión posterior."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addWidget(self._build_algoritmo_group())
        layout.addWidget(self._build_modelo_group())
        layout.addWidget(self._build_restricciones_group())
        layout.addLayout(self._build_actions())
        layout.addStretch()

    def _build_algoritmo_group(self) -> QGroupBox:
        group = QGroupBox("Parámetros del algoritmo")
        form = QFormLayout(group)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.c1_input = QLineEdit("2.0")
        self.c2_input = QLineEdit("2.0")
        self.w_input = QLineEdit("0.9")
        self.vmax_input = QLineEdit("1.5")
        self.n_particles_input = QLineEdit("150")
        self.max_iter_input = QLineEdit("150")

        self._set_read_only(
            self.c1_input,
            self.c2_input,
            self.w_input,
            self.vmax_input,
            self.n_particles_input,
            self.max_iter_input,
        )

        form.addRow("c1", self.c1_input)
        form.addRow("c2", self.c2_input)
        form.addRow("w", self.w_input)
        form.addRow("v_max", self.vmax_input)
        form.addRow("N partículas", self.n_particles_input)
        form.addRow("Max iter", self.max_iter_input)

        return group

    def _build_modelo_group(self) -> QGroupBox:
        group = QGroupBox("Parámetros del modelo")
        form = QFormLayout(group)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.rend_ch4_input = QLineEdit("1.01")
        self.rend_ch6_input = QLineEdit("0.59")
        self.v_inicio_input = QLineEdit("0.85")
        self.v_final_input = QLineEdit("0.85")

        self._set_read_only(
            self.rend_ch4_input,
            self.rend_ch6_input,
            self.v_inicio_input,
            self.v_final_input,
        )

        form.addRow("Rendimiento CH4", self.rend_ch4_input)
        form.addRow("Rendimiento CH6", self.rend_ch6_input)
        form.addRow("Factor volumen inicial", self.v_inicio_input)
        form.addRow("Factor volumen final", self.v_final_input)

        return group

    def _build_restricciones_group(self) -> QGroupBox:
        group = QGroupBox("Restricciones operativas")
        form = QFormLayout(group)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.v_cincel_max_input = QLineEdit("190000.0")
        self.v_cincel_min_input = QLineEdit("20000.0")
        self.v_camp_max_input = QLineEdit("90000.0")
        self.v_camp_min_input = QLineEdit("20000.0")
        self.q_rango_min_input = QLineEdit("6.0")
        self.q_rango_max_input = QLineEdit("15.0")

        self._set_read_only(
            self.v_cincel_max_input,
            self.v_cincel_min_input,
            self.v_camp_max_input,
            self.v_camp_min_input,
            self.q_rango_min_input,
            self.q_rango_max_input,
        )

        form.addRow("V Cincel max", self.v_cincel_max_input)
        form.addRow("V Cincel min", self.v_cincel_min_input)
        form.addRow("V Campanario max", self.v_camp_max_input)
        form.addRow("V Campanario min", self.v_camp_min_input)
        form.addRow("Q rango min", self.q_rango_min_input)
        form.addRow("Q rango max", self.q_rango_max_input)

        return group

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.restore_btn = QPushButton("Restaurar valores por defecto")
        self.restore_btn.setEnabled(False)

        self.save_btn = QPushButton("Guardar cambios")
        self.save_btn.setEnabled(False)

        actions.addStretch()
        actions.addWidget(self.restore_btn)
        actions.addWidget(self.save_btn)

        return actions

    def _set_read_only(self, *inputs: QLineEdit) -> None:
        for widget in inputs:
            widget.setReadOnly(True)