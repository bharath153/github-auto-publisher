"""Entry point for GitHub Auto-Publisher."""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from gui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("GitHub Auto-Publisher")
    app.setApplicationDisplayName("🚀 GitHub Auto-Publisher")

    # Apply global stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ffffff;
        }
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 10px;
            padding: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #24292f;
        }
        QLineEdit {
            padding: 8px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            background: #ffffff;
        }
        QLineEdit:focus {
            border-color: #0969da;
        }
        QComboBox {
            padding: 8px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            background: #ffffff;
        }
        QCheckBox {
            spacing: 8px;
        }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
