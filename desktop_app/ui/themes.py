def get_dark_stylesheet() -> str:
    return """
    QMainWindow, QDialog {
        background-color: #17191D;
        color: #F2F4F8;
    }

    QWidget {
        color: #F2F4F8;
    }

    QScrollArea, QScrollArea > QWidget > QWidget {
        background-color: #17191D;
    }

    QMenuBar {
        background-color: #17191D;
        color: #F2F4F8;
        border-bottom: 1px solid #2D3440;
    }

    QMenuBar::item {
        padding: 6px 10px;
    }

    QMenuBar::item:selected {
        background-color: #1F232A;
    }

    QMenu {
        background-color: #1F232A;
        color: #F2F4F8;
        border: 1px solid #2D3440;
    }

    QMenu::item:selected {
        background-color: #123E7C;
        color: #FFFFFF;
    }

    QMessageBox {
        background-color: #17191D;
        color: #F2F4F8;
    }

    QFrame#ActivityBar {
        background-color: #0F1318;
        border-right: 1px solid #2D3440;
    }

    QToolButton {
        background-color: transparent;
        border: none;
        border-left: 3px solid transparent;
        border-radius: 6px;
        padding: 8px;
    }

    QToolButton:hover {
        background-color: #1F232A;
        border-left: 3px solid #E8D85A;
    }

    QToolButton:checked {
        background-color: #123E7C;
        border-left: 3px solid #F2D313;
    }

    QGroupBox {
        border: 1px solid #3A4454;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 12px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
        color: #F2F4F8;
    }

    QLineEdit, QTextEdit, QDateEdit, QComboBox, QTableWidget {
        background-color: #1F232A;
        color: #F2F4F8;
        border: 1px solid #3A4454;
        border-radius: 4px;
        padding: 4px;
    }

    QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
        border: 1px solid #4C8DFF;
    }

    QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {
        background-color: #262C35;
        color: #C7D0DB;
        border: 1px solid #3A4454;
    }

    QComboBox:disabled, QDateEdit:disabled, QLineEdit:disabled, QTextEdit:disabled {
        background-color: #2A2F38;
        color: #7E8794;
        border: 1px solid #3A4454;
    }

    QComboBox::drop-down {
        border: none;
        width: 22px;
    }

    QCheckBox {
        spacing: 8px;
        color: #F2F4F8;
    }

    QCheckBox:disabled {
        color: #7E8794;
    }

    QTableWidget {
        gridline-color: #2D3440;
        alternate-background-color: #1B2027;
        selection-background-color: #123E7C;
        selection-color: #FFFFFF;
    }

    QHeaderView::section {
        background-color: #1F232A;
        color: #F2F4F8;
        padding: 6px;
        border: 1px solid #2D3440;
        font-weight: 600;
    }

    QTableWidget::item:selected {
        background-color: #123E7C;
        color: #FFFFFF;
    }

    QTableCornerButton::section {
        background-color: #1F232A;
        border: 1px solid #2D3440;
    }

    QPushButton {
        background-color: #123E7C;
        color: #FFFFFF;
        border: 1px solid #1E5BB8;
        border-radius: 4px;
        padding: 6px 12px;
    }

    QPushButton:hover {
        background-color: #1E5BB8;
    }

    QPushButton:pressed {
        background-color: #0D2E5C;
    }

    QPushButton:disabled {
        background-color: #2A2F38;
        color: #7E8794;
        border: 1px solid #3A4454;
    }

    QStatusBar {
        min-height: 24px;
        background-color: #0F1318;
        color: #F2F4F8;
        border-top: 1px solid #2D3440;
    }

    QStatusBar::item {
        border: none;
    }

    QLabel#PageTitle {
        color: #F2F4F8;
        font-size: 24px;
        font-weight: 600;
    }

    QLabel#PageSubtitle {
        color: #A9B3C2;
    }

    QLabel#StatusPanel {
        background-color: #1F232A;
        color: #F2F4F8;
        border: 1px solid #3A4454;
        border-radius: 4px;
        padding: 10px;
    }

    QLabel#LoginErrorLabel {
        color: #FF8E8E;
        font-weight: 600;
        padding-top: 2px;
    }

    QTabWidget::pane {
        border: 1px solid #2F4F7F;
        background: #111827;
        top: -1px;
    }

    QTabBar::tab {
        background: #1B2430;
        color: #DBE7FF;
        border: 1px solid #2F4F7F;
        padding: 8px 14px;
        min-width: 90px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #0F172A;
        color: #FFFFFF;
        font-weight: 600;
        border-bottom-color: #0F172A;
    }

    QTabBar::tab:hover:!selected {
        background: #23324A;
    }
    """


def get_light_stylesheet() -> str:
    return """
    QMainWindow, QDialog {
        background-color: #F6F8FB;
        color: #1C2430;
    }

    QWidget {
        color: #1C2430;
    }

    QScrollArea, QScrollArea > QWidget > QWidget {
        background-color: #F6F8FB;
    }

    QMenuBar {
        background-color: #F6F8FB;
        color: #1C2430;
        border-bottom: 1px solid #D6DDE8;
    }

    QMenuBar::item {
        padding: 6px 10px;
    }

    QMenuBar::item:selected {
        background-color: #E8EEF7;
    }

    QMenu {
        background-color: #FFFFFF;
        color: #1C2430;
        border: 1px solid #D6DDE8;
    }

    QMenu::item:selected {
        background-color: #DCE8FB;
        color: #123E7C;
    }

    QMessageBox {
        background-color: #F6F8FB;
        color: #1C2430;
    }

    QFrame#ActivityBar {
        background-color: #EEF3F9;
        border-right: 1px solid #D6DDE8;
    }

    QToolButton {
        background-color: transparent;
        border: none;
        border-left: 3px solid transparent;
        border-radius: 6px;
        padding: 8px;
    }

    QToolButton:hover {
        background-color: #E8EEF7;
        border-left: 3px solid #E8D85A;
    }

    QToolButton:checked {
        background-color: #DCE8FB;
        border-left: 3px solid #F2D313;
    }

    QGroupBox {
        border: 1px solid #D6DDE8;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 12px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
        color: #1C2430;
    }

    QLineEdit, QTextEdit, QDateEdit, QComboBox, QTableWidget {
        background-color: #FFFFFF;
        color: #1C2430;
        border: 1px solid #C7D1DE;
        border-radius: 4px;
        padding: 4px;
    }

    QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
        border: 1px solid #4C8DFF;
    }

    QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {
        background-color: #F1F4F8;
        color: #5E6B7A;
        border: 1px solid #D6DDE8;
    }

    QComboBox:disabled, QDateEdit:disabled, QLineEdit:disabled, QTextEdit:disabled {
        background-color: #EEF1F5;
        color: #8A94A3;
        border: 1px solid #D6DDE8;
    }

    QComboBox::drop-down {
        border: none;
        width: 22px;
    }

    QCheckBox {
        spacing: 8px;
        color: #1C2430;
    }

    QCheckBox:disabled {
        color: #8A94A3;
    }

    QTableWidget {
        gridline-color: #D6DDE8;
        alternate-background-color: #F7F9FC;
        selection-background-color: #DCE8FB;
        selection-color: #123E7C;
    }

    QHeaderView::section {
        background-color: #EEF3F9;
        color: #1C2430;
        padding: 6px;
        border: 1px solid #D6DDE8;
        font-weight: 600;
    }

    QTableWidget::item:selected {
        background-color: #DCE8FB;
        color: #123E7C;
    }

    QTableCornerButton::section {
        background-color: #EEF3F9;
        border: 1px solid #D6DDE8;
    }

    QPushButton {
        background-color: #123E7C;
        color: #FFFFFF;
        border: 1px solid #1E5BB8;
        border-radius: 4px;
        padding: 6px 12px;
    }

    QPushButton:hover {
        background-color: #1E5BB8;
    }

    QPushButton:pressed {
        background-color: #0D2E5C;
    }

    QPushButton:disabled {
        background-color: #EEF1F5;
        color: #8A94A3;
        border: 1px solid #D6DDE8;
    }

    QStatusBar {
        min-height: 24px;
        background-color: #EEF3F9;
        color: #1C2430;
        border-top: 1px solid #D6DDE8;
    }

    QStatusBar::item {
        border: none;
    }

    QLabel#PageTitle {
        color: #123E7C;
        font-size: 24px;
        font-weight: 600;
    }

    QLabel#PageSubtitle {
        color: #5E6B7A;
    }

    QLabel#StatusPanel {
        background-color: #FFFFFF;
        color: #1C2430;
        border: 1px solid #D6DDE8;
        border-radius: 4px;
        padding: 10px;
    }

    QLabel#LoginErrorLabel {
        color: #C23B3B;
        font-weight: 600;
        padding-top: 2px;
    }

    QTabWidget::pane {
        border: 1px solid #C7CFDB;
        background: #FFFFFF;
        top: -1px;
    }

    QTabBar::tab {
        background: #E9EDF3;
        color: #1F3B64;
        border: 1px solid #C7CFDB;
        padding: 8px 14px;
        min-width: 90px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #FFFFFF;
        color: #123E7C;
        font-weight: 600;
        border-bottom-color: #FFFFFF;
    }

    QTabBar::tab:hover:!selected {
        background: #DFE6EF;
        color: #123E7C;
    }
    """