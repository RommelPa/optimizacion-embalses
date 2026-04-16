from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from services.corrida_local_service import CorridaLocalService


class NuevaCorridaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.on_refresh_historial: Callable[[], None] | None = None
        self.on_open_detail: Callable[[str], None] | None = None
        self._build_ui()

    def set_after_create_callbacks(
        self,
        on_refresh_historial: Callable[[], None] | None = None,
        on_open_detail: Callable[[str], None] | None = None,
    ) -> None:
        self.on_refresh_historial = on_refresh_historial
        self.on_open_detail = on_open_detail

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Nueva corrida")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)

        form_group = QGroupBox("Datos de la corrida")
        form_layout = QFormLayout(form_group)

        self.caso_estudio_input = QLineEdit()
        self.caso_estudio_input.setPlaceholderText("Ej. Base abril 2026 - excel legacy")

        self.modo_operacion_input = QComboBox()
        self.modo_operacion_input.addItems(["inicial", "reprograma"])

        self.fecha_proceso_input = QDateEdit()
        self.fecha_proceso_input.setCalendarPopup(True)
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.fecha_proceso_input.setDisplayFormat("yyyy-MM-dd")

        self.escenario_input = QComboBox()
        self.escenario_input.addItems(["base"])

        self.origen_datos_input = QComboBox()
        self.origen_datos_input.addItems(["excel", "manual"])
        self.origen_datos_input.currentTextChanged.connect(self._on_origen_changed)

        self.archivo_entrada_input = QLineEdit()
        self.archivo_entrada_input.setReadOnly(True)

        archivo_layout = QHBoxLayout()
        archivo_layout.addWidget(self.archivo_entrada_input)

        self.buscar_archivo_btn = QPushButton("Seleccionar Excel")
        self.buscar_archivo_btn.clicked.connect(self._select_excel_file)
        archivo_layout.addWidget(self.buscar_archivo_btn)

        self.observaciones_input = QTextEdit()
        self.observaciones_input.setFixedHeight(100)

        form_layout.addRow("Caso de estudio", self.caso_estudio_input)
        form_layout.addRow("Modo operación", self.modo_operacion_input)
        form_layout.addRow("Fecha proceso", self.fecha_proceso_input)
        form_layout.addRow("Escenario", self.escenario_input)
        form_layout.addRow("Origen datos", self.origen_datos_input)
        form_layout.addRow("Archivo entrada", archivo_layout)
        form_layout.addRow("Observaciones", self.observaciones_input)

        layout.addWidget(form_group)

        self.crear_btn = QPushButton("Crear corrida")
        self.crear_btn.clicked.connect(self._submit)
        layout.addWidget(self.crear_btn)

        self.resultado_label = QLabel("")
        self.resultado_label.setWordWrap(True)
        layout.addWidget(self.resultado_label)

        layout.addStretch()
        self._on_origen_changed(self.origen_datos_input.currentText())

    def _on_origen_changed(self, origen: str) -> None:
        requiere_excel = origen == "excel"
        self.archivo_entrada_input.setEnabled(requiere_excel)
        self.buscar_archivo_btn.setEnabled(requiere_excel)

        if not requiere_excel:
            self.archivo_entrada_input.clear()

    def _select_excel_file(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Excel",
            "",
            "Excel (*.xlsx *.xlsm *.xls)",
        )
        if filepath:
            self.archivo_entrada_input.setText(filepath)

    def _clear_form(self) -> None:
        self.caso_estudio_input.clear()
        self.modo_operacion_input.setCurrentText("inicial")
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.escenario_input.setCurrentText("base")
        self.origen_datos_input.setCurrentText("excel")
        self.archivo_entrada_input.clear()
        self.observaciones_input.clear()

    def _submit(self) -> None:
        caso_estudio = self.caso_estudio_input.text().strip()
        modo_operacion = self.modo_operacion_input.currentText()
        fecha_proceso = self.fecha_proceso_input.date().toString("yyyy-MM-dd")
        escenario = self.escenario_input.currentText()
        origen_datos = self.origen_datos_input.currentText()
        archivo_entrada = self.archivo_entrada_input.text().strip() or None
        observaciones = self.observaciones_input.toPlainText().strip() or None

        if not caso_estudio:
            QMessageBox.warning(self, "Validación", "Caso de estudio es obligatorio.")
            return

        if origen_datos == "excel" and not archivo_entrada:
            QMessageBox.warning(self, "Validación", "Debes seleccionar un archivo Excel.")
            return

        if origen_datos == "manual":
            archivo_entrada = None

        try:
            result = self.service.crear_corrida(
                caso_estudio=caso_estudio,
                modo_operacion=modo_operacion,
                fecha_proceso=fecha_proceso,
                escenario=escenario,
                origen_datos=origen_datos,
                observaciones=observaciones,
                archivo_entrada=archivo_entrada,
            )
            data = result.get("data", {})
            corrida_id = data.get("id", "")
            self.resultado_label.setText(
                f"Corrida creada correctamente.\n"
                f"ID: {corrida_id or '-'}\n"
                f"Caso de estudio: {data.get('caso_estudio', '-')}\n"
                f"Estado: {data.get('estado', '-')}"
            )

            if self.on_refresh_historial:
                self.on_refresh_historial()

            self._clear_form()

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Éxito")
            msg.setText("Corrida creada correctamente.")
            abrir_btn = msg.addButton("Abrir detalle", QMessageBox.AcceptRole)
            msg.addButton("Cerrar", QMessageBox.RejectRole)
            msg.exec()

            if msg.clickedButton() == abrir_btn and corrida_id and self.on_open_detail:
                self.on_open_detail(corrida_id)

        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo crear la corrida:\n{exc}")