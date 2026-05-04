from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from services.auth_local_service import AuthLocalService


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.auth_service = AuthLocalService()
        self.authenticated_user = None
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Iniciar sesión")
        self.setModal(True)
        self.setFixedWidth(420)
        self.setSizeGripEnabled(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Iniciar sesión")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Ingrese sus credenciales para continuar.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.returnPressed.connect(self._focus_password)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self._login)

        form.addRow("Usuario", self.username_input)
        form.addRow("Contraseña", self.password_input)
        layout.addLayout(form)

        self.show_password_checkbox = QCheckBox("Mostrar contraseña")
        self.show_password_checkbox.toggled.connect(self._toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        self.error_label.setObjectName("LoginErrorLabel")
        layout.addWidget(self.error_label)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addStretch()

        self.cancel_btn = QPushButton("Salir")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setAutoDefault(False)

        self.login_btn = QPushButton("Ingresar")
        self.login_btn.clicked.connect(self._login)
        self.login_btn.setDefault(True)

        actions.addWidget(self.cancel_btn)
        actions.addWidget(self.login_btn)
        layout.addLayout(actions)

        self.username_input.textChanged.connect(self._clear_error)
        self.password_input.textChanged.connect(self._clear_error)

        self.username_input.setFocus()

    def _focus_password(self) -> None:
        self.password_input.setFocus()

    def _toggle_password_visibility(self, checked: bool) -> None:
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        )

    def _set_error(self, message: str) -> None:
        text = message.strip()
        self.error_label.setText(text)
        self.error_label.setVisible(bool(text))

    def _clear_error(self) -> None:
        self.error_label.clear()
        self.error_label.setVisible(False)

    def _login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text()

        self._clear_error()

        try:
            self.authenticated_user = self.auth_service.autenticar(username, password)
            self.accept()
        except ValueError as exc:
            self._set_error(str(exc))
            self.password_input.selectAll()
            self.password_input.setFocus()
        except Exception:
            self._set_error("No se pudo iniciar sesión. Intente nuevamente.")
            self.password_input.selectAll()
            self.password_input.setFocus()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)