from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
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
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Inicio de sesión")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Ingrese sus credenciales para acceder al sistema de optimización de embalses."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self._login)

        form.addRow("Usuario", self.username_input)
        form.addRow("Contraseña", self.password_input)
        layout.addLayout(form)

        actions = QHBoxLayout()
        actions.addStretch()

        self.cancel_btn = QPushButton("Salir")
        self.cancel_btn.clicked.connect(self.reject)

        self.login_btn = QPushButton("Ingresar")
        self.login_btn.clicked.connect(self._login)
        self.login_btn.setDefault(True)

        actions.addWidget(self.cancel_btn)
        actions.addWidget(self.login_btn)
        layout.addLayout(actions)

        helper = QLabel(
            "Usuarios iniciales de prueba: operador / operador123  |  ingeniero / ingeniero123"
        )
        helper.setObjectName("PageSubtitle")
        helper.setWordWrap(True)
        helper.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(helper)

    def _login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text()

        try:
            self.authenticated_user = self.auth_service.autenticar(username, password)
            self.accept()
        except Exception as exc:
            QMessageBox.warning(self, "Autenticación", str(exc))