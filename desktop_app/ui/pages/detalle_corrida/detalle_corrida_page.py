from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from services.corrida_local_service import CorridaLocalService
from ui.pages.detalle_corrida.tabs.configuracion_tab import ConfiguracionTab
from ui.pages.detalle_corrida.tabs.resumen_tab import ResumenTab
from ui.pages.detalle_corrida.tabs.resultados_tab import ResultadosTab


class DetalleCorridaPage(QWidget):
    def __init__(self, user_session) -> None:
        super().__init__()
        self.user_session = user_session
        self.service = CorridaLocalService()
        self.current_corrida_id: str | None = None
        self.current_caso_estudio: str | None = None
        self.current_detail: dict | None = None
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

        title = QLabel("Detalle de corrida")
        title.setObjectName("PageTitle")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "Revise la corrida seleccionada, sus datos principales, "
            "la configuración usada, las observaciones y la auditoría de ejecución."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        self.caso_base_status_label = QLabel("Esta corrida no es el caso base global.")
        self.caso_base_status_label.setObjectName("StatusPanel")
        self.caso_base_status_label.setWordWrap(True)
        main_layout.addWidget(self.caso_base_status_label)

        self.main_tabs = QTabWidget()
        self.resumen_tab = ResumenTab()
        self.resultados_tab = ResultadosTab()
        self.configuracion_tab = ConfiguracionTab()

        self.main_tabs.addTab(self.resumen_tab, "Resumen")
        self.main_tabs.addTab(self.resultados_tab, "Resultados")
        self.main_tabs.addTab(self.configuracion_tab, "Configuración usada")

        main_layout.addWidget(self.main_tabs)
        main_layout.addLayout(self._build_actions())
        main_layout.addStretch()

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.marcar_caso_base_btn = QPushButton("Marcar como caso base")
        self.marcar_caso_base_btn.setMinimumHeight(34)
        self.marcar_caso_base_btn.clicked.connect(self.marcar_como_caso_base)

        rol = getattr(self.user_session, "rol", "").strip().lower()
        self.marcar_caso_base_btn.setVisible(rol == "ingeniero")

        self.export_btn = QPushButton("Exportar Excel")
        self.export_btn.setMinimumHeight(34)
        self.export_btn.clicked.connect(self.export_excel)

        actions.addStretch()
        actions.addWidget(self.marcar_caso_base_btn)
        actions.addWidget(self.export_btn)
        return actions

    def load_corrida(self, corrida_id: str) -> None:
        detail = self.service.obtener_corrida(corrida_id)
        self.current_corrida_id = corrida_id
        self.current_caso_estudio = detail.get("caso_estudio", "")
        self.current_detail = detail

        self.resumen_tab.set_detail(detail)
        self.resultados_tab.set_detail(detail)
        self.configuracion_tab.set_configuracion(
            detail.get("configuracion_usada", {}) or {}
        )
        self._refresh_caso_base_status(detail)

    def _refresh_caso_base_status(self, detail: dict) -> None:
        es_caso_base = bool(detail.get("es_caso_base", False))
        estado = str(detail.get("estado", "")).strip().lower()

        if es_caso_base:
            self.caso_base_status_label.setText(
                "Esta corrida es el caso base global actual."
            )
        else:
            self.caso_base_status_label.setText(
                "Esta corrida no es el caso base global."
            )

        rol = getattr(self.user_session, "rol", "").strip().lower()
        if rol == "ingeniero":
            self.marcar_caso_base_btn.setEnabled(
                estado == "completada" and not es_caso_base
            )

    def marcar_como_caso_base(self) -> None:
        if not self.current_corrida_id:
            QMessageBox.warning(self, "Validación", "No hay corrida cargada.")
            return

        if self.current_detail is None:
            QMessageBox.warning(self, "Validación", "No hay detalle cargado.")
            return

        if self.current_detail.get("es_caso_base", False):
            QMessageBox.information(
                self,
                "Caso base",
                "La corrida actual ya es el caso base global.",
            )
            return

        if str(self.current_detail.get("estado", "")).strip().lower() != "completada":
            QMessageBox.warning(
                self,
                "Caso base",
                "Solo una corrida completada puede marcarse como caso base.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Marcar caso base",
            "¿Deseas marcar esta corrida como caso base global?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.marcar_como_caso_base(
                self.current_corrida_id,
                self.user_session,
            )
            self.load_corrida(self.current_corrida_id)

            parent_window = self.window()
            set_status_message = getattr(parent_window, "set_status_message", None)
            if callable(set_status_message):
                set_status_message("Caso base global actualizado")

            QMessageBox.information(
                self,
                "Éxito",
                "La corrida fue marcada como caso base global.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo marcar la corrida como caso base:\n{exc}",
            )

    def export_excel(self) -> None:
        if not self.current_corrida_id:
            QMessageBox.warning(self, "Validación", "No hay corrida cargada.")
            return

        caso = (self.current_caso_estudio or "corrida").strip()
        caso_sanitizado = "".join(
            ch if ch.isalnum() or ch in ("-", "_") else "_"
            for ch in caso
        ).strip("_")
        caso_sanitizado = caso_sanitizado[:40] or "corrida"
        sugerido = f"{caso_sanitizado}_{self.current_corrida_id[:8]}.xlsx"

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            sugerido,
            "Excel (*.xlsx)",
        )
        if not filepath:
            return

        try:
            self.service.descargar_excel(self.current_corrida_id, Path(filepath))
            QMessageBox.information(self, "Éxito", "Excel exportado correctamente.")
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo exportar el Excel:\n{exc}",
            )