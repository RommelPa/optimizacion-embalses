from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.pages.configuracion_page import ConfiguracionPage
from ui.pages.detalle_corrida_page import DetalleCorridaPage
from ui.pages.historial_page import HistorialPage
from ui.pages.nueva_corrida_page import NuevaCorridaPage
from ui.themes import get_dark_stylesheet, get_light_stylesheet

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Optimización Embalses - Escritorio")
        self.resize(1280, 800)

        self.page_nueva_corrida = 0
        self.page_historial = 1
        self.page_detalle = 2
        self.page_configuracion = 3

        self.nav_buttons: dict[str, QToolButton] = {}

        self._build_actions()
        self._build_ui()
        self._build_menu()
        self._build_pages()
        self._wire_pages()

        self.apply_dark_theme()
        self.show_nueva_corrida_page()

    def _build_actions(self) -> None:
        self.action_nueva_corrida = QAction("Nueva corrida", self)
        self.action_nueva_corrida.triggered.connect(self.show_nueva_corrida_page)

        self.action_historial = QAction("Historial", self)
        self.action_historial.triggered.connect(self.show_historial_page)

        self.action_detalle = QAction("Detalle actual", self)
        self.action_detalle.triggered.connect(self.show_detalle_page)

        self.action_configuracion = QAction("Configuración", self)
        self.action_configuracion.triggered.connect(self.show_configuracion_page)

        self.action_tema_claro = QAction("Modo claro", self)
        self.action_tema_claro.triggered.connect(self.apply_light_theme)

        self.action_tema_oscuro = QAction("Modo oscuro", self)
        self.action_tema_oscuro.triggered.connect(self.apply_dark_theme)

        self.action_salir = QAction("Salir", self)
        self.action_salir.triggered.connect(self.close)

        self.action_acerca_de = QAction("Acerca de", self)
        self.action_acerca_de.triggered.connect(self._show_about_dialog)

    def _build_ui(self) -> None:
        self._build_status_bar()

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.root_layout = QHBoxLayout(self.central)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        self._build_activity_bar()

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.root_layout.addWidget(self.activity_bar)
        self.root_layout.addWidget(self.stack, 1)

    def _build_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setMinimumHeight(24)
        self.status_bar.showMessage("Listo", 0)

    def _build_activity_bar(self) -> None:
        self.activity_bar = QFrame()
        self.activity_bar.setObjectName("ActivityBar")
        self.activity_bar.setFixedWidth(64)

        layout = QVBoxLayout(self.activity_bar)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(8)

        self.btn_nav_nueva = self._create_nav_button(
            tooltip="Nueva corrida",
            icon=self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder),
            callback=self.show_nueva_corrida_page,
        )
        self.btn_nav_historial = self._create_nav_button(
            tooltip="Historial",
            icon=self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView),
            callback=self.show_historial_page,
        )
        self.btn_nav_detalle = self._create_nav_button(
            tooltip="Detalle actual",
            icon=self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView),
            callback=self.show_detalle_page,
        )
        self.btn_nav_config = self._create_nav_button(
            tooltip="Configuración",
            icon=self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon),
            callback=self.show_configuracion_page,
        )

        self.nav_buttons = {
            "nueva": self.btn_nav_nueva,
            "historial": self.btn_nav_historial,
            "detalle": self.btn_nav_detalle,
            "configuracion": self.btn_nav_config,
        }

        layout.addWidget(self.btn_nav_nueva)
        layout.addWidget(self.btn_nav_historial)
        layout.addWidget(self.btn_nav_detalle)
        layout.addWidget(self.btn_nav_config)
        layout.addStretch()

    def _create_nav_button(
        self,
        tooltip: str,
        icon,
        callback,
    ) -> QToolButton:
        btn = QToolButton()
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn.setIcon(icon)
        btn.setIconSize(QSize(20, 20))
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumSize(44, 44)
        btn.clicked.connect(callback)
        return btn

    def _build_menu(self) -> None:
        menu_bar = self.menuBar()

        archivo_menu = menu_bar.addMenu("Archivo")
        ayuda_menu = menu_bar.addMenu("Ayuda")

        menu_tema = QMenu("Tema", self)
        menu_tema.addAction(self.action_tema_claro)
        menu_tema.addAction(self.action_tema_oscuro)

        archivo_menu.addAction(self.action_nueva_corrida)
        archivo_menu.addAction(self.action_historial)
        archivo_menu.addAction(self.action_detalle)
        archivo_menu.addAction(self.action_configuracion)
        archivo_menu.addMenu(menu_tema)
        archivo_menu.addSeparator()
        archivo_menu.addAction(self.action_salir)

        ayuda_menu.addAction(self.action_acerca_de)

    def _build_pages(self) -> None:
        self.nueva_corrida_page = NuevaCorridaPage()
        self.historial_page = HistorialPage(on_open_detail=self.open_detail_page)
        self.detalle_page = DetalleCorridaPage()
        self.configuracion_page = ConfiguracionPage()

        self.stack.addWidget(self.nueva_corrida_page)
        self.stack.addWidget(self.historial_page)
        self.stack.addWidget(self.detalle_page)
        self.stack.addWidget(self.configuracion_page)

    def _wire_pages(self) -> None:
        self.nueva_corrida_page.set_after_create_callbacks(
            on_refresh_historial=self._refresh_historial_from_create,
            on_open_detail=self.open_detail_page,
        )

    def set_status_message(self, message: str, timeout_ms: int = 4000) -> None:
        self.status_bar.showMessage(message, timeout_ms)

    def _refresh_historial_from_create(self) -> None:
        self.historial_page.load_data()
        self.set_status_message("Historial actualizado")

    def _set_active_nav(self, key: str) -> None:
        button = self.nav_buttons.get(key)
        if button is not None:
            button.setChecked(True)

    def show_nueva_corrida_page(self) -> None:
        self.stack.setCurrentIndex(self.page_nueva_corrida)
        self._set_active_nav("nueva")
        self.set_status_message("Vista: Nueva corrida")

    def show_historial_page(self) -> None:
        self.historial_page.load_data()
        self.stack.setCurrentIndex(self.page_historial)
        self._set_active_nav("historial")
        self.set_status_message("Vista: Historial")

    def show_detalle_page(self) -> None:
        self.stack.setCurrentIndex(self.page_detalle)
        self._set_active_nav("detalle")
        self.set_status_message("Vista: Detalle")

    def show_configuracion_page(self) -> None:
        self.stack.setCurrentIndex(self.page_configuracion)
        self._set_active_nav("configuracion")
        self.set_status_message("Vista: Configuración")

    def open_detail_page(self, corrida_id: str) -> None:
        try:
            self.detalle_page.load_corrida(corrida_id)
            self.stack.setCurrentIndex(self.page_detalle)
            self._set_active_nav("detalle")
            self.set_status_message(f"Detalle cargado: {corrida_id[:8]}")
        except Exception as exc:
            self.set_status_message("Error al abrir detalle", 6000)
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo abrir el detalle:\n{exc}",
            )

    def apply_dark_theme(self) -> None:
        self.setStyleSheet(get_dark_stylesheet())
        self.set_status_message("Tema aplicado: oscuro", 3000)

    def apply_light_theme(self) -> None:
        self.setStyleSheet(get_light_stylesheet())
        self.set_status_message("Tema aplicado: claro", 3000)

    def _show_about_dialog(self) -> None:
        QMessageBox.information(
            self,
            "Acerca de",
            "Optimización Embalses\nAplicación de escritorio para ejecución de corridas PSO.",
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        worker_thread = self.nueva_corrida_page.worker_thread

        if worker_thread is not None and worker_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmar salida",
                "Hay una corrida en ejecución. ¿Deseas cerrar la aplicación?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        event.accept()