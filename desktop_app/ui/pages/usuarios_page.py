from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.usuario_local_service import UsuarioLocalService


class UsuariosPage(QWidget):
    def __init__(self, user_session) -> None:
        super().__init__()
        self.user_session = user_session
        self.service = UsuarioLocalService()
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

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Usuarios")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Administre usuarios del sistema, sus roles, estado y restablecimiento de contraseña."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addWidget(self._build_create_group())
        layout.addWidget(self._build_table_group())
        layout.addLayout(self._build_actions())
        layout.addStretch()

    def _build_create_group(self) -> QGroupBox:
        group = QGroupBox("Crear usuario")
        form = QFormLayout(group)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nuevo usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña inicial")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.rol_input = QComboBox()
        self.rol_input.addItems(["operador", "ingeniero"])

        self.crear_btn = QPushButton("Crear usuario")
        self.crear_btn.clicked.connect(self._crear_usuario)

        row_actions = QHBoxLayout()
        row_actions.addWidget(self.crear_btn)
        row_actions.addStretch()

        form.addRow("Usuario", self.username_input)
        form.addRow("Contraseña", self.password_input)
        form.addRow("Rol", self.rol_input)
        form.addRow("", row_actions)

        return group

    def _build_table_group(self) -> QGroupBox:
        group = QGroupBox("Usuarios registrados")
        layout = QVBoxLayout(group)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            [
                "Usuario",
                "Rol",
                "Estado",
                "Creado",
                "Último login",
                "ID",
            ]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(False)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setColumnHidden(5, True)

        layout.addWidget(self.table)
        return group

    def _build_actions(self) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_data)

        self.cambiar_rol_btn = QPushButton("Cambiar rol")
        self.cambiar_rol_btn.clicked.connect(self._cambiar_rol)

        self.toggle_estado_btn = QPushButton("Activar / Inactivar")
        self.toggle_estado_btn.clicked.connect(self._cambiar_estado)

        self.reset_password_btn = QPushButton("Resetear contraseña")
        self.reset_password_btn.clicked.connect(self._resetear_password)

        actions.addWidget(self.refresh_btn)
        actions.addWidget(self.cambiar_rol_btn)
        actions.addWidget(self.toggle_estado_btn)
        actions.addWidget(self.reset_password_btn)
        actions.addStretch()

        return actions

    def load_data(self) -> None:
        try:
            self.items_cache = self.service.listar_usuarios(self.user_session)
            self._render_table(self.items_cache)
        except (ValueError, PermissionError) as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))
        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo cargar la lista de usuarios. Intente nuevamente.",
            )

    def _render_table(self, items: list[dict]) -> None:
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table.setRowCount(len(items))

        for row_idx, item in enumerate(items):
            values = [
                str(item.get("username", "")),
                str(item.get("rol", "")),
                "activo" if item.get("activo", False) else "inactivo",
                self._format_datetime(item.get("created_at")),
                self._format_datetime(item.get("ultimo_login_at")),
                str(item.get("id", "")),
            ]

            for col_idx, value in enumerate(values):
                table_item = QTableWidgetItem(value)
                table_item.setToolTip(value)

                if col_idx == 5:
                    table_item.setData(Qt.ItemDataRole.UserRole, item.get("id"))

                self.table.setItem(row_idx, col_idx, table_item)

        if items:
            self.table.selectRow(0)

    def _crear_usuario(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text()
        rol = self.rol_input.currentText()

        try:
            self.service.crear_usuario(
                self.user_session,
                username=username,
                password=password,
                rol=rol,
            )
            self.username_input.clear()
            self.password_input.clear()
            self.rol_input.setCurrentText("operador")
            self.load_data()
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente.")
        except (ValueError, PermissionError) as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))
        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el usuario. Intente nuevamente.",
            )

    def _cambiar_rol(self) -> None:
        selected = self._get_selected_usuario()
        if selected is None:
            return

        usuario_id, username, rol_actual, _activo = selected
        nuevo_rol = "ingeniero" if rol_actual == "operador" else "operador"

        reply = QMessageBox.question(
            self,
            "Cambiar rol",
            f"¿Deseas cambiar el rol de '{username}' a '{nuevo_rol}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.cambiar_rol(
                self.user_session,
                usuario_id=usuario_id,
                nuevo_rol=nuevo_rol,
            )
            self.load_data()
            QMessageBox.information(self, "Éxito", "Rol actualizado correctamente.")
        except (ValueError, PermissionError) as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))
        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo cambiar el rol. Intente nuevamente.",
            )

    def _cambiar_estado(self) -> None:
        selected = self._get_selected_usuario()
        if selected is None:
            return

        usuario_id, username, _rol, activo = selected
        nuevo_estado = not activo
        texto_estado = "activar" if nuevo_estado else "inactivar"

        reply = QMessageBox.question(
            self,
            "Cambiar estado",
            f"¿Deseas {texto_estado} al usuario '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.cambiar_estado(
                self.user_session,
                usuario_id=usuario_id,
                activo=nuevo_estado,
            )
            self.load_data()
            QMessageBox.information(self, "Éxito", "Estado actualizado correctamente.")
        except (ValueError, PermissionError) as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))
        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo cambiar el estado. Intente nuevamente.",
            )

    def _resetear_password(self) -> None:
        selected = self._get_selected_usuario()
        if selected is None:
            return

        usuario_id, username, _rol, _activo = selected

        nueva_password = self.password_input.text()
        if not nueva_password.strip():
            QMessageBox.warning(
                self,
                "Usuarios",
                "Escribe una contraseña en el campo 'Contraseña' para resetearla.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Resetear contraseña",
            f"¿Deseas resetear la contraseña del usuario '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.resetear_password(
                self.user_session,
                usuario_id=usuario_id,
                nueva_password=nueva_password,
            )
            self.password_input.clear()
            QMessageBox.information(self, "Éxito", "Contraseña reseteada correctamente.")
        except (ValueError, PermissionError) as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))
        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo resetear la contraseña. Intente nuevamente.",
            )

    def _get_selected_usuario(self) -> tuple[int, str, str, bool] | None:
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Usuarios", "Selecciona un usuario.")
            return None

        username_item = self.table.item(current_row, 0)
        rol_item = self.table.item(current_row, 1)
        estado_item = self.table.item(current_row, 2)
        id_item = self.table.item(current_row, 5)

        if (
            username_item is None
            or rol_item is None
            or estado_item is None
            or id_item is None
        ):
            QMessageBox.warning(self, "Usuarios", "No se pudo leer el usuario seleccionado.")
            return None

        usuario_id = int(id_item.text())
        username = username_item.text()
        rol = rol_item.text()
        activo = estado_item.text().strip().lower() == "activo"

        return usuario_id, username, rol, activo

    def _format_datetime(self, value) -> str:
        if value is None:
            return "-"

        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")

        text = str(value).strip()
        if not text:
            return "-"

        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return text