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

from ui.pages.detalle_corrida.formatters import format_int, format_number


class ConfiguracionTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addWidget(self._build_configuracion_group())
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

    def set_configuracion(self, data: dict) -> None:
        self._set_label_value(self.cfg_c1_label, format_number(data.get("c1"), 4))
        self._set_label_value(self.cfg_c2_label, format_number(data.get("c2"), 4))
        self._set_label_value(self.cfg_w_label, format_number(data.get("w"), 4))
        self._set_label_value(self.cfg_v_max_label, format_number(data.get("v_max"), 4))
        self._set_label_value(self.cfg_n_particles_label, format_int(data.get("n_particles")))
        self._set_label_value(self.cfg_max_iter_label, format_int(data.get("max_iter")))

        self._set_label_value(
            self.cfg_rend_ch4_label,
            format_number(data.get("rendimiento_ch4"), 4),
        )
        self._set_label_value(
            self.cfg_rend_ch6_label,
            format_number(data.get("rendimiento_ch6"), 4),
        )
        self._set_label_value(
            self.cfg_v_inicio_label,
            format_number(data.get("v_inicio_factor"), 4),
        )
        self._set_label_value(
            self.cfg_v_final_label,
            format_number(data.get("v_final_factor"), 4),
        )

        self._set_label_value(
            self.cfg_v_cincel_max_label,
            format_number(data.get("v_cincel_max"), 2),
        )
        self._set_label_value(
            self.cfg_v_cincel_min_label,
            format_number(data.get("v_cincel_min"), 2),
        )
        self._set_label_value(
            self.cfg_v_camp_max_label,
            format_number(data.get("v_campanario_max"), 2),
        )
        self._set_label_value(
            self.cfg_v_camp_min_label,
            format_number(data.get("v_campanario_min"), 2),
        )
        self._set_label_value(
            self.cfg_q_min_label,
            format_number(data.get("q_rango_min"), 4),
        )
        self._set_label_value(
            self.cfg_q_max_label,
            format_number(data.get("q_rango_max"), 4),
        )