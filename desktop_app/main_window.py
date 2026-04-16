from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QWidget,
)

from ui.pages.detalle_corrida_page import DetalleCorridaPage
from ui.pages.historial_page import HistorialPage
from ui.pages.nueva_corrida_page import NuevaCorridaPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Optimización Embalses - Escritorio")
        self.resize(1280, 800)

        self._build_ui()
        self._wire_pages()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.addItem(QListWidgetItem("Nueva corrida"))
        self.sidebar.addItem(QListWidgetItem("Historial"))
        self.sidebar.addItem(QListWidgetItem("Detalle"))
        self.sidebar.currentRowChanged.connect(self._on_nav_changed)

        self.page_container = QWidget()
        self.page_layout = QHBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.nueva_corrida_page = NuevaCorridaPage()
        self.historial_page = HistorialPage(on_open_detail=self.open_detail_page)
        self.detalle_page = DetalleCorridaPage()

        self.pages = [
            self.nueva_corrida_page,
            self.historial_page,
            self.detalle_page,
        ]

        for page in self.pages:
            page.setVisible(False)
            self.page_layout.addWidget(page)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.page_container)

        self.sidebar.setCurrentRow(0)
        self._show_page(0)

    def _wire_pages(self) -> None:
        self.nueva_corrida_page.set_after_create_callbacks(
            on_refresh_historial=self.historial_page.load_data,
            on_open_detail=self.open_detail_page,
        )

    def _on_nav_changed(self, index: int) -> None:
        if index < 0:
            return
        self._show_page(index)

    def _show_page(self, index: int) -> None:
        for i, page in enumerate(self.pages):
            page.setVisible(i == index)

    def open_detail_page(self, corrida_id: str) -> None:
        try:
            self.detalle_page.load_corrida(corrida_id)
            self.sidebar.setCurrentRow(2)
            self._show_page(2)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el detalle:\n{exc}")