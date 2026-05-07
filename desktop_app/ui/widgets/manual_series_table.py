from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class ManualSeriesTable(QTableWidget):
    def __init__(self, row_count: int = 48, parent: QWidget | None = None) -> None:
        super().__init__(row_count, 3, parent)
        self.row_count_expected = row_count
        self._build_ui()

    def _build_ui(self) -> None:
        self.setHorizontalHeaderLabels(["Hora", "CMG", "P_CHAR 5"])
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(False)

        header = self.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.setColumnWidth(0, 90)

        for row in range(self.rowCount()):
            hora_item = QTableWidgetItem(self._build_hour_label(row))
            hora_item.setFlags(hora_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            hora_item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            )
            self.setItem(row, 0, hora_item)

            self._get_or_create_editable_item(row, 1)
            self._get_or_create_editable_item(row, 2)

    def _get_or_create_editable_item(self, row: int, column: int) -> QTableWidgetItem:
        item = self.item(row, column)
        if item is None:
            item = QTableWidgetItem("")
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.setItem(row, column, item)
        return item

    def _build_hour_label(self, index: int) -> str:
        total_minutes = (index + 1) * 30
        hour = total_minutes // 60
        minute = total_minutes % 60
        return "24:00" if hour == 24 and minute == 0 else f"{hour:02d}:{minute:02d}"

    def clear_series(self) -> None:
        for row in range(self.rowCount()):
            for column in (1, 2):
                item = self._get_or_create_editable_item(row, column)
                item.setText("")

    def set_series(self, cmg: list[float], p_char_5: list[float]) -> None:
        self.clear_series()

        if len(cmg) != self.row_count_expected:
            raise ValueError(
                f"La serie CMG debe tener {self.row_count_expected} valores."
            )
        if len(p_char_5) != self.row_count_expected:
            raise ValueError(
                f"La serie P_CHAR 5 debe tener {self.row_count_expected} valores."
            )

        for row, value in enumerate(cmg):
            item = self._get_or_create_editable_item(row, 1)
            item.setText(str(value))

        for row, value in enumerate(p_char_5):
            item = self._get_or_create_editable_item(row, 2)
            item.setText(str(value))

    def validate_series(self) -> list[str]:
        errors: list[str] = []

        for column, name in ((1, "CMG"), (2, "P_CHAR 5")):
            values_in_column: list[float] = []

            for row in range(self.rowCount()):
                item = self.item(row, column)
                text = item.text().strip() if item else ""

                if not text:
                    errors.append(f"La columna {name} contiene celdas vacías.")
                    break

                try:
                    value = float(text)
                except ValueError:
                    errors.append(f"La columna {name} contiene valores no numéricos.")
                    break

                if column == 2 and value < 0:
                    errors.append("La columna P_CHAR 5 no puede contener valores negativos.")
                    break

                values_in_column.append(value)

            if len(values_in_column) != self.row_count_expected and not errors:
                errors.append(
                    f"La columna {name} debe tener {self.row_count_expected} valores."
                )

        return errors

        return errors

    def get_series_data(self) -> tuple[list[float], list[float]]:
        errors = self.validate_series()
        if errors:
            raise ValueError(errors[0])

        cmg: list[float] = []
        p_char_5: list[float] = []

        for row in range(self.rowCount()):
            cmg_item = self.item(row, 1)
            p_char_item = self.item(row, 2)

            if cmg_item is None or p_char_item is None:
                raise ValueError("La tabla de series está incompleta.")

            cmg.append(float(cmg_item.text().strip()))
            p_char_5.append(float(p_char_item.text().strip()))

        return cmg, p_char_5

    def keyPressEvent(self, event) -> None:
        if event.matches(QKeySequence.StandardKey.Paste):
            self._paste_from_clipboard()
            return

        super().keyPressEvent(event)

    def _paste_from_clipboard(self) -> None:
        text = QApplication.clipboard().text().strip()
        if not text:
            return

        matrix = self._parse_clipboard_matrix(text)
        if not matrix:
            return

        start_row = self.currentRow()
        start_col = self.currentColumn()

        if start_row < 0:
            start_row = 0

        if start_col not in (1, 2):
            QMessageBox.warning(
                self,
                "Pegar datos",
                "Selecciona una celda en la columna CMG o P_CHAR 5 antes de pegar.",
            )
            return

        pasted_cols = max(len(row) for row in matrix)

        if pasted_cols > 2:
            QMessageBox.warning(
                self,
                "Pegar datos",
                "Solo se permiten hasta 2 columnas: CMG y P_CHAR 5.",
            )
            return

        if pasted_cols == 2 and start_col != 1:
            QMessageBox.warning(
                self,
                "Pegar datos",
                "Para pegar dos columnas, selecciona una celda de la columna CMG.",
            )
            return

        if start_row + len(matrix) > self.rowCount():
            QMessageBox.warning(
                self,
                "Pegar datos",
                "La cantidad de filas pegadas excede el número de períodos disponibles.",
            )
            return

        for row_offset, row_values in enumerate(matrix):
            target_row = start_row + row_offset

            for col_offset, value in enumerate(row_values):
                target_col = start_col + col_offset

                if target_col not in (1, 2):
                    continue

                item = self._get_or_create_editable_item(target_row, target_col)
                item.setText(value.strip())

    def _parse_clipboard_matrix(self, text: str) -> list[list[str]]:
        rows_raw = [row for row in text.splitlines() if row.strip()]
        matrix: list[list[str]] = []

        for row in rows_raw:
            cols = row.split("\t")
            matrix.append(cols)

        return matrix