from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QThread, Qt
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
    QScrollArea,
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

        title = QLabel("Nueva corrida")
        title.setObjectName("PageTitle")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "Ejecute una nueva corrida a partir del archivo Excel oficial "
            "y revise el resultado en el historial o en el detalle."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        main_layout.addWidget(self._build_form_group())
        main_layout.addLayout(self._build_actions())
        main_layout.addWidget(self._build_result_group())
        main_layout.addStretch()

    def _build_form_group(self) -> QGroupBox:
        form_group = QGroupBox("Datos de la corrida")
        form_layout = QFormLayout(form_group)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(12)
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.caso_estudio_input = QLineEdit()
        self.caso_estudio_input.setPlaceholderText(
            "Ej. Base abril 2026 - validación manual"
        )

        self.modo_operacion_value = "inicial"
        self.modo_operacion_label = QLabel("inicial")
        self.modo_operacion_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.fecha_proceso_input = QDateEdit()
        self.fecha_proceso_input.setCalendarPopup(True)
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.fecha_proceso_input.setDisplayFormat("yyyy-MM-dd")

        self.escenario_value = "base"
        self.escenario_label = QLabel("base")
        self.escenario_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.origen_datos_value = "excel"
        self.origen_datos_label = QLabel("excel")
        self.origen_datos_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.archivo_entrada_input = QLineEdit()
        self.archivo_entrada_input.setReadOnly(True)
        self.archivo_entrada_input.setPlaceholderText("Seleccione un archivo Excel...")

        archivo_layout = QHBoxLayout()
        archivo_layout.setSpacing(8)
        archivo_layout.addWidget(self.archivo_entrada_input)

        self.buscar_archivo_btn = QPushButton("Seleccionar Excel")
        self.buscar_archivo_btn.clicked.connect(self._select_excel_file)
        archivo_layout.addWidget(self.buscar_archivo_btn)

        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMinimumHeight(110)
        self.observaciones_input.setPlaceholderText(
            "Ingrese observaciones opcionales para esta corrida."
        )

        form_layout.addRow("Caso de estudio", self.caso_estudio_input)
        form_layout.addRow("Modo de operación", self.modo_operacion_label)
        form_layout.addRow("Fecha de proceso", self.fecha_proceso_input)
        form_layout.addRow("Escenario", self.escenario_label)
        form_layout.addRow("Origen de datos", self.origen_datos_label)
        form_layout.addRow("Archivo de entrada", archivo_layout)
        form_layout.addRow("Observaciones", self.observaciones_input)

        return form_group

    def _build_actions(self) -> QHBoxLayout:
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.crear_btn = QPushButton("Crear corrida")
        self.crear_btn.setMinimumHeight(34)
        self.crear_btn.clicked.connect(self._submit)

        self.limpiar_btn = QPushButton("Limpiar")
        self.limpiar_btn.setMinimumHeight(34)
        self.limpiar_btn.clicked.connect(lambda: self._clear_form(reset_result=True))

        actions_layout.addStretch()
        actions_layout.addWidget(self.limpiar_btn)
        actions_layout.addWidget(self.crear_btn)

        return actions_layout

    def _build_result_group(self) -> QGroupBox:
        result_group = QGroupBox("Estado de ejecución")
        result_layout = QVBoxLayout(result_group)

        self.resultado_label = QLabel("Sin ejecución reciente.")
        self.resultado_label.setObjectName("StatusPanel")
        self.resultado_label.setWordWrap(True)
        self.resultado_label.setMinimumHeight(70)
        self.resultado_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.resultado_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        result_layout.addWidget(self.resultado_label)
        return result_group

    def _set_form_enabled(self, enabled: bool) -> None:
        self.caso_estudio_input.setEnabled(enabled)
        self.fecha_proceso_input.setEnabled(enabled)
        self.observaciones_input.setEnabled(enabled)
        self.archivo_entrada_input.setEnabled(enabled)
        self.buscar_archivo_btn.setEnabled(enabled)
        self.crear_btn.setEnabled(enabled)
        self.limpiar_btn.setEnabled(enabled)

    def _select_excel_file(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Excel",
            "",
            "Excel (*.xlsx *.xlsm *.xls)",
        )
        if filepath:
            self.archivo_entrada_input.setText(filepath)

    def _reset_form_fields(self) -> None:
        self.caso_estudio_input.clear()
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.archivo_entrada_input.clear()
        self.observaciones_input.clear()

    def _clear_form(self, reset_result: bool = False) -> None:
        if self.worker_thread is not None and self.worker_thread.isRunning():
            QMessageBox.warning(
                self,
                "Validación",
                "No se puede limpiar el formulario mientras hay una corrida en ejecución.",
            )
            return

        self._reset_form_fields()

        if reset_result:
            self.resultado_label.setText("Sin ejecución reciente.")

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
            QMessageBox.warning(
                self,
                "Validación",
                "Debes seleccionar un archivo Excel.",
            )
            return

        self._set_form_enabled(False)
        self.resultado_label.setText(
            "Estado actual: ejecutando...\n"
            "Ejecutando corrida..."
        )

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

        self._reset_form_fields()
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
            "Estado actual: error.\n"
            "La corrida no pudo completarse."
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