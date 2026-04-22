from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from services.configuracion_local_service import ConfiguracionLocalService


class ConfiguracionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.service = ConfiguracionLocalService()
        self._build_ui()
        self._load_configuracion()

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
            "Edite la configuración global del sistema. "
            "Estos valores serán usados por las próximas corridas."
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

        self.c1_input = QLineEdit()
        self.c2_input = QLineEdit()
        self.w_input = QLineEdit()
        self.vmax_input = QLineEdit()
        self.n_particles_input = QLineEdit()
        self.max_iter_input = QLineEdit()

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

        self.rend_ch4_input = QLineEdit()
        self.rend_ch6_input = QLineEdit()
        self.v_inicio_input = QLineEdit()
        self.v_final_input = QLineEdit()

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

        self.v_cincel_max_input = QLineEdit()
        self.v_cincel_min_input = QLineEdit()
        self.v_camp_max_input = QLineEdit()
        self.v_camp_min_input = QLineEdit()
        self.q_rango_min_input = QLineEdit()
        self.q_rango_max_input = QLineEdit()

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
        self.restore_btn.clicked.connect(self._restore_defaults)

        self.save_btn = QPushButton("Guardar cambios")
        self.save_btn.clicked.connect(self._save_configuracion)

        actions.addStretch()
        actions.addWidget(self.restore_btn)
        actions.addWidget(self.save_btn)

        return actions

    def _get_payload(self) -> dict:
        return {
            "c1": self.c1_input.text().strip(),
            "c2": self.c2_input.text().strip(),
            "w": self.w_input.text().strip(),
            "v_max": self.vmax_input.text().strip(),
            "n_particles": self.n_particles_input.text().strip(),
            "max_iter": self.max_iter_input.text().strip(),
            "rendimiento_ch4": self.rend_ch4_input.text().strip(),
            "rendimiento_ch6": self.rend_ch6_input.text().strip(),
            "v_inicio_factor": self.v_inicio_input.text().strip(),
            "v_final_factor": self.v_final_input.text().strip(),
            "v_cincel_max": self.v_cincel_max_input.text().strip(),
            "v_cincel_min": self.v_cincel_min_input.text().strip(),
            "v_campanario_max": self.v_camp_max_input.text().strip(),
            "v_campanario_min": self.v_camp_min_input.text().strip(),
            "q_rango_min": self.q_rango_min_input.text().strip(),
            "q_rango_max": self.q_rango_max_input.text().strip(),
        }

    def _set_payload(self, data: dict) -> None:
        self.c1_input.setText(str(data.get("c1", "")))
        self.c2_input.setText(str(data.get("c2", "")))
        self.w_input.setText(str(data.get("w", "")))
        self.vmax_input.setText(str(data.get("v_max", "")))
        self.n_particles_input.setText(str(data.get("n_particles", "")))
        self.max_iter_input.setText(str(data.get("max_iter", "")))

        self.rend_ch4_input.setText(str(data.get("rendimiento_ch4", "")))
        self.rend_ch6_input.setText(str(data.get("rendimiento_ch6", "")))
        self.v_inicio_input.setText(str(data.get("v_inicio_factor", "")))
        self.v_final_input.setText(str(data.get("v_final_factor", "")))

        self.v_cincel_max_input.setText(str(data.get("v_cincel_max", "")))
        self.v_cincel_min_input.setText(str(data.get("v_cincel_min", "")))
        self.v_camp_max_input.setText(str(data.get("v_campanario_max", "")))
        self.v_camp_min_input.setText(str(data.get("v_campanario_min", "")))
        self.q_rango_min_input.setText(str(data.get("q_rango_min", "")))
        self.q_rango_max_input.setText(str(data.get("q_rango_max", "")))

    def _load_configuracion(self) -> None:
        try:
            data = self.service.obtener_configuracion()
            self._set_payload(data)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar la configuración:\n{exc}",
            )

    def _save_configuracion(self) -> None:
        try:
            payload = self._get_payload()
            saved = self.service.guardar_configuracion(payload)
            self._set_payload(saved)

            parent_window = self.window()
            set_status_message = getattr(parent_window, "set_status_message", None)
            if callable(set_status_message):
                set_status_message("Configuración guardada correctamente")

            QMessageBox.information(
                self,
                "Éxito",
                "La configuración fue guardada correctamente.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo guardar la configuración:\n{exc}",
            )

    def _restore_defaults(self) -> None:
        reply = QMessageBox.question(
            self,
            "Confirmar restauración",
            "¿Deseas restaurar los valores por defecto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            data = self.service.restaurar_configuracion_por_defecto()
            self._set_payload(data)

            parent_window = self.window()
            set_status_message = getattr(parent_window, "set_status_message", None)
            if callable(set_status_message):
                set_status_message("Configuración restaurada por defecto")

            QMessageBox.information(
                self,
                "Éxito",
                "La configuración fue restaurada a sus valores por defecto.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo restaurar la configuración:\n{exc}",
            )