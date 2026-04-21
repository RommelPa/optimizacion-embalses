from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
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
        layout = QVBoxLayout(self)

        title = QLabel("Historial")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)

        filtros_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por ID o caso de estudio")
        self.search_input.returnPressed.connect(self.apply_filters)
        filtros_layout.addWidget(self.search_input)

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

        actions = QHBoxLayout()
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_data)
        actions.addWidget(self.refresh_btn)
        actions.addStretch()
        layout.addLayout(actions)

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
        self.table.doubleClicked.connect(self._open_selected_detail)
        layout.addWidget(self.table)

        self.open_btn = QPushButton("Abrir detalle")
        self.open_btn.clicked.connect(self._open_selected_detail)
        layout.addWidget(self.open_btn)

        self.summary_label = QLabel("")
        layout.addWidget(self.summary_label)

        self.load_data()

    def load_data(self) -> None:
        try:
            result = self.service.listar_corridas()
            self.items_cache = result.get("items", [])
            self.apply_filters()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el historial:\n{exc}")

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
            f"Mostrando {len(filtered_items)} de {len(self.items_cache)} corridas registradas."
        )

    def clear_filters(self) -> None:
        self.search_input.clear()
        self.estado_filter.setCurrentText("Todos")
        self.origen_filter.setCurrentText("Todos")
        self.apply_filters()

    def _render_table(self, items: list[dict]) -> None:
        self.table.clearContents()
        self.table.setRowCount(len(items))

        for row_idx, item in enumerate(items):
            values = [
                item.get("id", ""),
                item.get("caso_estudio", ""),
                item.get("fecha_proceso", ""),
                item.get("modo_operacion", ""),
                item.get("origen_datos", ""),
                item.get("estado", ""),
                str(item.get("best_cost", "")),
                str(item.get("execution_time_sec", "")),
            ]
            for col_idx, value in enumerate(values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()
        if items:
            self.table.selectRow(0)

    def _open_selected_detail(self) -> None:
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Validación", "Selecciona una corrida.")
            return

        corrida_id_item = self.table.item(current_row, 0)
        if corrida_id_item is None:
            QMessageBox.warning(self, "Validación", "No se encontró el ID de la corrida.")
            return

        self.on_open_detail(corrida_id_item.text())