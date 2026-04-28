from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.pages.detalle_corrida.formatters import format_number
from app.application.corrida_chart_builder import (
    render_caudal_chart,
    render_despacho_chart,
    render_volumenes_chart,
)

class ResultadosTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.results_tabs = QTabWidget()

        self.results_tabs.addTab(self._build_table_tab(), "Tabla")
        self.results_tabs.addTab(self._build_caudal_tab(), "Caudal")
        self.results_tabs.addTab(self._build_volumenes_tab(), "Volúmenes")
        self.results_tabs.addTab(self._build_despacho_tab(), "Despacho económico")

        layout.addWidget(self.results_tabs)

    def _build_table_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(
            [
                "HORA",
                "P_Char 5 (MW)",
                "Volumen D. Cincel (m3)",
                "Caudal Salida D. Cincel (m3/s)",
                "Volumen D. Campanario (m3)",
                "Caudal salida D. Campanario (m3/s)",
                "CH 4 (MW)",
                "CH 6 (MW)",
                "CMG (S/./MWh)",
            ]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(False)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)

        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(6, 105)
        self.table.setColumnWidth(7, 105)
        self.table.setColumnWidth(8, 140)

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive)

        self.table.setColumnWidth(2, 190)
        self.table.setColumnWidth(3, 240)
        self.table.setColumnWidth(4, 230)
        self.table.setColumnWidth(5, 270)

        layout.addWidget(self.table)
        return tab

    def _build_caudal_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.caudal_figure = Figure(figsize=(10, 5))
        self.caudal_canvas = FigureCanvas(self.caudal_figure)

        layout.addWidget(self.caudal_canvas)
        return tab
    
    def _build_volumenes_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.volumenes_figure = Figure(figsize=(10, 5))
        self.volumenes_canvas = FigureCanvas(self.volumenes_figure)

        layout.addWidget(self.volumenes_canvas)
        return tab
    
    def _build_despacho_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.despacho_figure = Figure(figsize=(10, 5))
        self.despacho_canvas = FigureCanvas(self.despacho_figure)

        layout.addWidget(self.despacho_canvas)
        return tab

    def set_detail(self, detail: dict) -> None:
        dataset = detail.get("resultados_dataset") or {}
        rows = self._build_table_rows(dataset)
        self._populate_table(rows)
        self._render_caudal_chart(dataset)
        self._render_volumenes_chart(dataset)
        self._render_despacho_chart(dataset)

    def _build_table_rows(self, dataset: dict) -> list[dict[str, str]]:
        if not dataset or "tabla" not in dataset:
            return []
        rows_src = dataset["tabla"]["rows"]
        rows: list[dict[str, str]] = []

        for row in rows_src:
            rows.append(
                {
                    "hora": row["hora"],
                    "p_char_5": format_number(row["p_char_5"], 2),
                    "v_cincel": format_number(row["v_cincel"], 2),
                    "q_opt": format_number(row["q_opt"], 3),
                    "v_campanario": format_number(row["v_campanario"], 2),
                    "q_campanario": format_number(row["q_salida_campanario"], 3),
                    "ch4": format_number(row["potencia_ch4"], 2),
                    "ch6": format_number(row["potencia_ch6"], 2),
                    "cmg": format_number(row["cmg"], 2),
                }
            )

        return rows

    def _populate_table(self, rows: list[dict[str, str]]) -> None:
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            values = [
                row["hora"],
                row["p_char_5"],
                row["v_cincel"],
                row["q_opt"],
                row["v_campanario"],
                row["q_campanario"],
                row["ch4"],
                row["ch6"],
                row["cmg"],
            ]

            for col_idx, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(value)

                if col_idx == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                    )
                else:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )

                self.table.setItem(row_idx, col_idx, item)

        if rows:
            self.table.selectRow(0)

    def _render_caudal_chart(self, dataset: dict) -> None:
        self.caudal_figure.clear()
        ax = self.caudal_figure.add_subplot(111)
        render_caudal_chart(ax, dataset)
        self.caudal_figure.tight_layout()
        self.caudal_canvas.draw()

    def _render_volumenes_chart(self, dataset: dict) -> None:
        self.volumenes_figure.clear()
        ax = self.volumenes_figure.add_subplot(111)
        render_volumenes_chart(ax, dataset)
        self.volumenes_figure.tight_layout()
        self.volumenes_canvas.draw()

    def _render_despacho_chart(self, dataset: dict) -> None:
        self.despacho_figure.clear()
        ax = self.despacho_figure.add_subplot(111)
        render_despacho_chart(ax, dataset)
        self.despacho_figure.tight_layout()
        self.despacho_canvas.draw()