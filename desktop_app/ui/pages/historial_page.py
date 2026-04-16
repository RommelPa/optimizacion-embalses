from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
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
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Historial")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)

        actions = QHBoxLayout()
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_data)
        actions.addWidget(self.refresh_btn)
        actions.addStretch()
        layout.addLayout(actions)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Caso de estudio",
                "Fecha proceso",
                "Origen",
                "Estado",
                "Best cost",
                "Tiempo (s)",
            ]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self._open_selected_detail)
        layout.addWidget(self.table)

        self.open_btn = QPushButton("Abrir detalle")
        self.open_btn.clicked.connect(self._open_selected_detail)
        layout.addWidget(self.open_btn)

        self.load_data()

    def load_data(self) -> None:
        try:
            result = self.service.listar_corridas()
            items = result.get("items", [])
            self.table.setRowCount(len(items))

            for row_idx, item in enumerate(items):
                values = [
                    item.get("id", ""),
                    item.get("caso_estudio", ""),
                    item.get("fecha_proceso", ""),
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
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el historial:\n{exc}")

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