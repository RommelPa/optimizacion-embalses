from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from services.corrida_local_service import CorridaLocalService


class HistorialPage(QWidget):
    def __init__(self, on_open_detail: Callable[[str], None]) -> None:
        super().__init__()
        self.service = CorridaLocalService()
        self.on_open_detail = on_open_detail
        self.items_cache: list[dict] = []
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

        title = QLabel("Historial")
        title.setObjectName("PageTitle")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "Consulte las corridas registradas, filtre resultados y abra el detalle "
            "de la corrida seleccionada."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        main_layout.addWidget(self._build_filters_group())
        main_layout.addWidget(self._build_table_group())
        main_layout.addStretch()

        self.load_data()

    def _build_filters_group(self) -> QGroupBox:
        group = QGroupBox("Filtros y acciones")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por ID o caso de estudio")
        self.search_input.returnPressed.connect(self.apply_filters)
        self.search_input.setMinimumWidth(320)
        filtros_layout.addWidget(self.search_input, 1)

        self.estado_filter = QComboBox()
        self.estado_filter.addItems(["Todos", "completada", "rechazada", "fallida"])
        self.estado_filter.currentTextChanged.connect(lambda _: self.apply_filters())
        filtros_layout.addWidget(self.estado_filter)

        self.origen_filter = QComboBox()
        self.origen_filter.addItems(["Todos", "excel"])
        self.origen_filter.currentTextChanged.connect(lambda _: self.apply_filters())
        filtros_layout.addWidget(self.origen_filter)

        self.filtrar_btn = QPushButton("Filtrar")
        self.filtrar_btn.clicked.connect(self.apply_filters)
        filtros_layout.addWidget(self.filtrar_btn)

        self.limpiar_btn = QPushButton("Limpiar")
        self.limpiar_btn.clicked.connect(self.clear_filters)
        filtros_layout.addWidget(self.limpiar_btn)

        layout.addLayout(filtros_layout)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_data)

        self.open_btn = QPushButton("Abrir detalle")
        self.open_btn.clicked.connect(self._open_selected_detail)

        actions_layout.addWidget(self.refresh_btn)
        actions_layout.addWidget(self.open_btn)
        actions_layout.addStretch()

        self.summary_label = QLabel("Sin datos cargados.")
        self.summary_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.summary_label.setObjectName("PageSubtitle")

        actions_layout.addWidget(self.summary_label)
        layout.addLayout(actions_layout)

        return group

    def _build_table_group(self) -> QGroupBox:
        group = QGroupBox("Corridas registradas")
        layout = QVBoxLayout(group)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Caso de estudio",
                "Fecha proceso",
                "Modo",
                "Origen",
                "Estado",
                "Mejor costo",
                "Tiempo (s)",
            ]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self._open_selected_detail)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)
        return group

    def load_data(self) -> None:
        try:
            result = self.service.listar_corridas()
            self.items_cache = result.get("items", [])
            self.apply_filters()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar el historial:\n{exc}",
            )

    def apply_filters(self) -> None:
        texto = self.search_input.text().strip().lower()
        estado = self.estado_filter.currentText()
        origen = self.origen_filter.currentText()

        filtered_items = []
        for item in self.items_cache:
            item_id = str(item.get("id", "")).lower()
            caso = str(item.get("caso_estudio", "")).lower()
            item_estado = str(item.get("estado", ""))
            item_origen = str(item.get("origen_datos", ""))

            match_texto = not texto or texto in item_id or texto in caso
            match_estado = estado == "Todos" or item_estado == estado
            match_origen = origen == "Todos" or item_origen == origen

            if match_texto and match_estado and match_origen:
                filtered_items.append(item)

        self._render_table(filtered_items)
        self.summary_label.setText(
            f"Mostrando {len(filtered_items)} de {len(self.items_cache)} corridas registradas"
        )

    def clear_filters(self) -> None:
        self.search_input.clear()
        self.estado_filter.setCurrentText("Todos")
        self.origen_filter.setCurrentText("Todos")
        self.apply_filters()

    def _render_table(self, items: list[dict]) -> None:
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table.setRowCount(len(items))

        for row_idx, item in enumerate(items):
            item_id = str(item.get("id", ""))
            item_id_short = item_id[:8]

            caso_estudio = str(item.get("caso_estudio", ""))
            fecha_proceso = str(item.get("fecha_proceso", ""))
            modo_operacion = str(item.get("modo_operacion", ""))
            origen_datos = str(item.get("origen_datos", ""))
            estado = str(item.get("estado", ""))

            best_cost_raw = item.get("best_cost", "")
            execution_time_raw = item.get("execution_time_sec", "")

            try:
                best_cost_text = (
                    f"{float(best_cost_raw):,.2f}"
                    if best_cost_raw not in ("", None)
                    else ""
                )
            except (ValueError, TypeError):
                best_cost_text = str(best_cost_raw)

            try:
                execution_time_text = (
                    f"{float(execution_time_raw):.2f}"
                    if execution_time_raw not in ("", None)
                    else ""
                )
            except (ValueError, TypeError):
                execution_time_text = str(execution_time_raw)

            values = [
                item_id_short,
                caso_estudio,
                fecha_proceso,
                modo_operacion,
                origen_datos,
                estado,
                best_cost_text,
                execution_time_text,
            ]

            tooltips = [
                item_id,
                caso_estudio,
                fecha_proceso,
                modo_operacion,
                origen_datos,
                estado,
                best_cost_text,
                execution_time_text,
            ]

            for col_idx, value in enumerate(values):
                table_item = QTableWidgetItem(value)
                table_item.setToolTip(tooltips[col_idx])

                if col_idx == 0:
                    table_item.setData(Qt.ItemDataRole.UserRole, item_id)

                self.table.setItem(row_idx, col_idx, table_item)

        if items:
            self.table.selectRow(0)

    def _open_selected_detail(self) -> None:
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Validación", "Selecciona una corrida.")
            return

        corrida_id_item = self.table.item(current_row, 0)
        if corrida_id_item is None:
            QMessageBox.warning(
                self,
                "Validación",
                "No se encontró el ID de la corrida.",
            )
            return

        corrida_id = corrida_id_item.data(Qt.ItemDataRole.UserRole)
        if not corrida_id:
            QMessageBox.warning(
                self,
                "Validación",
                "No se encontró el ID real de la corrida.",
            )
            return

        self.on_open_detail(str(corrida_id))