import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from PySide6.QtWidgets import QApplication

from app.db.init_db import init_db
from main_window import MainWindow
from ui.login_window import LoginWindow


def main() -> None:
    init_db()

    app = QApplication(sys.argv)

    while True:
        login = LoginWindow()
        login_result = login.exec()

        if (
            login_result != LoginWindow.DialogCode.Accepted
            or login.authenticated_user is None
        ):
            break

        window = MainWindow(login.authenticated_user)
        window.show()
        app.exec()

        if getattr(window, "logout_requested", False):
            continue

        break

    sys.exit(0)


if __name__ == "__main__":
    main()