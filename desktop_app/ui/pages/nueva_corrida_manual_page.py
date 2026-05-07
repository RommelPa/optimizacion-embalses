from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QThread, Qt
from PySide6.QtWidgets import (
    QDateEdit,
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

from services.corrida_local_service import CorridaLocalService
from ui.widgets.manual_series_table import ManualSeriesTable
from workers.corrida_manual_worker import CorridaManualWorker


class NuevaCorridaManualPage(QWidget):
    def __init__(self, user_session) -> None:
        super().__init__()
        self.user_session = user_session
        self.service = CorridaLocalService()
        self.on_refresh_historial: Callable[[], None] | None = None
        self.on_open_detail: Callable[[str], None] | None = None
        self.worker_thread: QThread | None = None
        self.worker: CorridaManualWorker | None = None
        self.current_caso_base_id: str | None = None
        self._build_ui()
        self._load_caso_base_summary()

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

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Nueva corrida manual")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Construya una corrida manual dentro de la aplicación, "
            "pegue series desde Excel y ejecute usando la configuración global vigente."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addWidget(self._build_form_group())
        layout.addWidget(self._build_caso_base_group())
        layout.addWidget(self._build_series_group())
        layout.addLayout(self._build_actions())
        layout.addWidget(self._build_result_group())
        layout.addStretch()

    def _build_form_group(self) -> QGroupBox:
        group = QGroupBox("Datos de la corrida")
        form = QFormLayout(group)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.caso_estudio_input = QLineEdit()
        self.caso_estudio_input.setPlaceholderText("Ej. Manual mayo 2026 - escenario base")

        self.modo_operacion_label = QLabel("inicial")
        self.modo_operacion_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.fecha_proceso_input = QDateEdit()
        self.fecha_proceso_input.setCalendarPopup(True)
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.fecha_proceso_input.setDisplayFormat("yyyy-MM-dd")

        self.escenario_input = QLineEdit()
        self.escenario_input.setText("base")

        self.origen_datos_label = QLabel("manual")
        self.origen_datos_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.q_salida_input = QLineEdit()
        self.q_salida_input.setPlaceholderText("Ej. 10.0")

        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMinimumHeight(100)
        self.observaciones_input.setPlaceholderText(
            "Ingrese observaciones opcionales para esta corrida manual."
        )

        form.addRow("Caso de estudio", self.caso_estudio_input)
        form.addRow("Modo de operación", self.modo_operacion_label)
        form.addRow("Fecha de proceso", self.fecha_proceso_input)
        form.addRow("Escenario", self.escenario_input)
        form.addRow("Origen de datos", self.origen_datos_label)
        form.addRow("Q salida Campanario", self.q_salida_input)
        form.addRow("Observaciones", self.observaciones_input)

        return group

    def _build_caso_base_group(self) -> QGroupBox:
        group = QGroupBox("Caso base global")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        self.caso_base_label = QLabel("No existe un caso base global disponible.")
        self.caso_base_label.setObjectName("StatusPanel")
        self.caso_base_label.setWordWrap(True)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.load_caso_base_btn = QPushButton("Cargar desde caso base")
        self.load_caso_base_btn.clicked.connect(self._load_from_caso_base)

        actions.addWidget(self.load_caso_base_btn)
        actions.addStretch()

        layout.addWidget(self.caso_base_label)
        layout.addLayout(actions)
        return group

    def _build_series_group(self) -> QGroupBox:
        group = QGroupBox("Series manuales")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        helper = QLabel(
            "Pegue una columna sobre CMG o P_CHAR 5, o pegue ambas columnas tabuladas desde Excel."
        )
        helper.setObjectName("PageSubtitle")
        helper.setWordWrap(True)

        self.series_table = ManualSeriesTable(row_count=48)

        table_actions = QHBoxLayout()
        table_actions.setSpacing(10)

        self.clear_series_btn = QPushButton("Limpiar tabla")
        self.clear_series_btn.clicked.connect(self.series_table.clear_series)

        table_actions.addWidget(self.clear_series_btn)
        table_actions.addStretch()

        layout.addWidget(helper)
        layout.addWidget(self.series_table)
        layout.addLayout(table_actions)

        return group

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.validar_btn = QPushButton("Validar")
        self.validar_btn.clicked.connect(self._validate_form)

        self.limpiar_btn = QPushButton("Limpiar")
        self.limpiar_btn.clicked.connect(lambda: self._clear_form(reset_result=True))

        self.crear_btn = QPushButton("Crear corrida")
        self.crear_btn.clicked.connect(self._submit)

        actions.addStretch()
        actions.addWidget(self.validar_btn)
        actions.addWidget(self.limpiar_btn)
        actions.addWidget(self.crear_btn)

        return actions

    def _build_result_group(self) -> QGroupBox:
        group = QGroupBox("Estado de ejecución")
        layout = QVBoxLayout(group)

        self.resultado_label = QLabel("Sin ejecución reciente.")
        self.resultado_label.setObjectName("StatusPanel")
        self.resultado_label.setWordWrap(True)
        self.resultado_label.setMinimumHeight(80)
        self.resultado_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.resultado_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(self.resultado_label)
        return group

    def _set_form_enabled(self, enabled: bool) -> None:
        self.caso_estudio_input.setEnabled(enabled)
        self.fecha_proceso_input.setEnabled(enabled)
        self.escenario_input.setEnabled(enabled)
        self.q_salida_input.setEnabled(enabled)
        self.observaciones_input.setEnabled(enabled)
        self.validar_btn.setEnabled(enabled)
        self.limpiar_btn.setEnabled(enabled)
        self.crear_btn.setEnabled(enabled)
        self.load_caso_base_btn.setEnabled(enabled)
        self.clear_series_btn.setEnabled(enabled)
        self.series_table.setEnabled(enabled)

    def _build_payload(self) -> dict:
        caso_estudio = self.caso_estudio_input.text().strip()
        escenario = self.escenario_input.text().strip()
        q_salida_text = self.q_salida_input.text().strip()
        observaciones = self.observaciones_input.toPlainText().strip() or None

        if not caso_estudio:
            raise ValueError("Caso de estudio es obligatorio.")

        if not escenario:
            raise ValueError("Escenario es obligatorio.")

        if not q_salida_text:
            raise ValueError("Q salida Campanario es obligatorio.")

        try:
            q_salida_campanario = float(q_salida_text)
        except ValueError as exc:
            raise ValueError("Q salida Campanario debe ser numérico.") from exc

        if q_salida_campanario <= 0:
            raise ValueError("Q salida Campanario debe ser mayor a 0.")

        series_errors = self.series_table.validate_series()
        if series_errors:
            raise ValueError(series_errors[0])

        cmg, p_char_5 = self.series_table.get_series_data()

        return {
            "caso_estudio": caso_estudio,
            "modo_operacion": "inicial",
            "fecha_proceso": self.fecha_proceso_input.date().toString("yyyy-MM-dd"),
            "escenario": escenario,
            "origen_datos": "manual",
            "usuario_id": self.user_session.id,
            "usuario_username": self.user_session.username,
            "usuario_rol": self.user_session.rol,
            "q_salida_campanario": q_salida_campanario,
            "cmg": cmg,
            "p_char_5": p_char_5,
            "observaciones": observaciones,
            "corrida_base_id": self.current_caso_base_id,
        }

    def _validate_form(self) -> None:
        try:
            payload = self._build_payload()
            self.resultado_label.setText(
                "Validación correcta.\n"
                f"Períodos: {len(payload['cmg'])}\n"
                f"Q salida Campanario: {payload['q_salida_campanario']:.3f}\n"
                f"Origen: {payload['origen_datos']}"
            )
        except ValueError as exc:
            QMessageBox.warning(self, "Validación", str(exc))

    def _submit(self) -> None:
        if self.worker_thread is not None and self.worker_thread.isRunning():
            QMessageBox.warning(
                self,
                "Validación",
                "Ya hay una corrida manual en ejecución.",
            )
            return

        try:
            payload = self._build_payload()
        except ValueError as exc:
            QMessageBox.warning(self, "Validación", str(exc))
            return

        self._set_form_enabled(False)
        self.resultado_label.setText(
            "Estado actual: ejecutando...\n"
            "Ejecutando corrida manual..."
        )

        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)
        if callable(set_status_message):
            set_status_message("Ejecutando corrida manual...", 0)

        self.worker_thread = QThread(self)
        self.worker = CorridaManualWorker(**payload)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_corrida_success)
        self.worker.error.connect(self._on_corrida_error)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)

        self.worker_thread.finished.connect(self._cleanup_worker_thread)

        self.worker_thread.start()

    def _on_corrida_success(self, result: dict) -> None:
        data = result.get("data", {})
        corrida_id = data.get("id", "")

        self.resultado_label.setText(
            f"Corrida manual creada correctamente.\n"
            f"ID: {corrida_id or '-'}\n"
            f"Caso de estudio: {data.get('caso_estudio', '-')}\n"
            f"Estado: {data.get('estado', '-')}\n"
            f"Tiempo (s): {data.get('execution_time_sec', '-')}"
        )

        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)
        if callable(set_status_message):
            set_status_message("Corrida manual creada correctamente")

        if self.on_refresh_historial:
            self.on_refresh_historial()

        self._reset_form_fields()
        self._set_form_enabled(True)
        self._load_caso_base_summary()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Éxito")
        msg.setText("Corrida manual creada correctamente.")
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
        self.resultado_label.setText(
            "Estado actual: error.\n"
            "La corrida manual no pudo completarse."
        )
        self._set_form_enabled(True)

        parent_window = self.window()
        set_status_message = getattr(parent_window, "set_status_message", None)
        if callable(set_status_message):
            set_status_message("Error al crear corrida manual", 6000)

        QMessageBox.critical(
            self,
            "Error",
            f"No se pudo crear la corrida manual:\n{error_message}",
        )

    def _cleanup_worker_thread(self) -> None:
        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

        if self.worker_thread is not None:
            self.worker_thread.deleteLater()
            self.worker_thread = None

    def _clear_form(self, reset_result: bool = False) -> None:
        if self.worker_thread is not None and self.worker_thread.isRunning():
            QMessageBox.warning(
                self,
                "Validación",
                "No se puede limpiar el formulario mientras hay una corrida en ejecución.",
            )
            return

        self._reset_form_fields()
        self._load_caso_base_summary()

        if reset_result:
            self.resultado_label.setText("Sin ejecución reciente.")

    def _load_caso_base_summary(self) -> None:
        try:
            caso_base = self.service.obtener_caso_base()
            if caso_base is None:
                self.current_caso_base_id = None
                self.caso_base_label.setText(
                    "No existe un caso base global disponible."
                )
                return

            self.current_caso_base_id = caso_base.get("id")
            self.caso_base_label.setText(
                f"Caso base actual: {caso_base.get('caso_estudio', '-')}\n"
                f"ID: {str(caso_base.get('id', '-'))[:8]}\n"
                f"Fecha proceso: {caso_base.get('fecha_proceso', '-')}\n"
                f"Origen: {caso_base.get('origen_datos', '-')}"
            )
        except Exception as exc:
            self.current_caso_base_id = None
            self.caso_base_label.setText(
                f"No se pudo cargar el caso base actual:\n{exc}"
            )

    def _load_from_caso_base(self) -> None:
        try:
            caso_base = self.service.obtener_caso_base()
            if caso_base is None:
                QMessageBox.warning(
                    self,
                    "Caso base",
                    "No existe un caso base global disponible.",
                )
                return

            cmg = caso_base.get("cmg", []) or []
            p_char_5 = caso_base.get("p_char_5", []) or []

            self.series_table.set_series(cmg, p_char_5)
            self.q_salida_input.setText(str(caso_base.get("q_salida_campanario", "")))
            self.escenario_input.setText(str(caso_base.get("escenario", "base")))

            if not self.caso_estudio_input.text().strip():
                base_name = str(caso_base.get("caso_estudio", "Caso base")).strip()
                self.caso_estudio_input.setText(f"{base_name} - manual")

            self.current_caso_base_id = caso_base.get("id")

            QMessageBox.information(
                self,
                "Caso base",
                "Se cargaron los datos del caso base actual.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar el caso base:\n{exc}",
            )

    def _reset_form_fields(self) -> None:
        self.caso_estudio_input.clear()
        self.fecha_proceso_input.setDate(QDate.currentDate())
        self.escenario_input.setText("base")
        self.q_salida_input.clear()
        self.observaciones_input.clear()
        self.series_table.clear_series()
        self.current_caso_base_id = None