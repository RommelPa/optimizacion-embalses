from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QThread
from PySide6.QtWidgets import (
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

from workers.corrida_worker import CorridaWorker


class NuevaCorridaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.on_refresh_historial: Callable[[], None] | None = None
        self.on_open_detail: Callable[[str], None] | None = None
        self.worker_thread: QThread | None = None
        self.worker: CorridaWorker | None = None
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
        self.caso_estudio_input.setPlaceholderText("Ej. Base abril 2026 - validación manual")

        self.modo_operacion_value = "inicial"
        self.modo_operacion_label = QLabel("inicial")

        self.fecha_proceso_input = QDateEdit()
        self.fecha_proceso_input.setCalendarPopup(True)
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.fecha_proceso_input.setDisplayFormat("yyyy-MM-dd")

        self.escenario_value = "base"
        self.escenario_label = QLabel("base")

        self.origen_datos_value = "excel"
        self.origen_datos_label = QLabel("excel")

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
        form_layout.addRow("Modo de operación", self.modo_operacion_label)
        form_layout.addRow("Fecha de proceso", self.fecha_proceso_input)
        form_layout.addRow("Escenario", self.escenario_label)
        form_layout.addRow("Origen de datos", self.origen_datos_label)
        form_layout.addRow("Archivo de entrada", archivo_layout)
        form_layout.addRow("Observaciones", self.observaciones_input)

        layout.addWidget(form_group)

        self.crear_btn = QPushButton("Crear corrida")
        self.crear_btn.clicked.connect(self._submit)
        layout.addWidget(self.crear_btn)

        self.resultado_label = QLabel("")
        self.resultado_label.setWordWrap(True)
        layout.addWidget(self.resultado_label)

        layout.addStretch()
        self.archivo_entrada_input.setEnabled(True)
        self.buscar_archivo_btn.setEnabled(True)

    def _set_form_enabled(self, enabled: bool) -> None:
        self.caso_estudio_input.setEnabled(enabled)
        self.fecha_proceso_input.setEnabled(enabled)
        self.observaciones_input.setEnabled(enabled)
        self.archivo_entrada_input.setEnabled(enabled)
        self.buscar_archivo_btn.setEnabled(enabled)
        self.crear_btn.setEnabled(enabled)

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
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.archivo_entrada_input.clear()
        self.observaciones_input.clear()

    def _submit(self) -> None:
        if self.worker_thread is not None and self.worker_thread.isRunning():
            QMessageBox.warning(
                self,
                "Validación",
                "Ya hay una corrida en ejecución.",
            )
            return
        caso_estudio = self.caso_estudio_input.text().strip()
        modo_operacion = self.modo_operacion_value
        fecha_proceso = self.fecha_proceso_input.date().toString("yyyy-MM-dd")
        escenario = self.escenario_value
        origen_datos = self.origen_datos_value
        archivo_entrada = self.archivo_entrada_input.text().strip() or None
        observaciones = self.observaciones_input.toPlainText().strip() or None

        if not caso_estudio:
            QMessageBox.warning(self, "Validación", "Caso de estudio es obligatorio.")
            return

        if not archivo_entrada:
            QMessageBox.warning(self, "Validación", "Debes seleccionar un archivo Excel.")
            return

        self._set_form_enabled(False)
        self.resultado_label.setText("Estado actual: ejecutando...\nEjecutando corrida...")

        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)
        if callable(set_status_message):
            set_status_message("Ejecutando corrida...", 0)

        self.worker_thread = QThread(self)
        self.worker = CorridaWorker(
            caso_estudio=caso_estudio,
            modo_operacion=modo_operacion,
            fecha_proceso=fecha_proceso,
            escenario=escenario,
            origen_datos=origen_datos,
            observaciones=observaciones,
            archivo_entrada=archivo_entrada,
        )
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_corrida_success)
        self.worker.error.connect(self._on_corrida_error)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)

        self.worker_thread.finished.connect(self._cleanup_worker_thread)

        self.worker_thread.start()

    def _on_corrida_success(self, result: dict) -> None:
        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)

        data = result.get("data", {})
        corrida_id = data.get("id", "")

        self.resultado_label.setText(
            f"Corrida creada correctamente.\n"
            f"ID: {corrida_id or '-'}\n"
            f"Caso de estudio: {data.get('caso_estudio', '-')}\n"
            f"Estado: {data.get('estado', '-')}\n"
            f"Tiempo (s): {data.get('execution_time_sec', '-')}"
        )

        if callable(set_status_message):
            set_status_message("Corrida creada correctamente")

        if self.on_refresh_historial:
            self.on_refresh_historial()

        self._clear_form()
        self._set_form_enabled(True)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Éxito")
        msg.setText("Corrida creada correctamente.")
        abrir_btn = msg.addButton(
            "Abrir detalle",
            QMessageBox.ButtonRole.AcceptRole,
        )
        msg.addButton(
            "Cerrar",
            QMessageBox.ButtonRole.RejectRole,
        )
        msg.exec()

        if msg.clickedButton() == abrir_btn and corrida_id and self.on_open_detail:
            self.on_open_detail(corrida_id)

    def _on_corrida_error(self, error_message: str) -> None:
        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)

        self.resultado_label.setText(
            "Estado actual: error.\nLa corrida no pudo completarse."
        )
        self._set_form_enabled(True)

        if callable(set_status_message):
            set_status_message("Error al crear corrida", 6000)

        QMessageBox.critical(
            self,
            "Error",
            f"No se pudo crear la corrida:\n{error_message}",
        )

    def _cleanup_worker_thread(self) -> None:
        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

        if self.worker_thread is not None:
            self.worker_thread.deleteLater()
            self.worker_thread = None