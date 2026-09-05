import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.window import CashBalance


# ============================================================
# ЗАПУСК
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Cash Balance"
    )

    app.setApplicationDisplayName(
        "Cash Balance"
    )

    # icon.ico находится рядом с main.py
    icon_path = (
        Path(__file__).resolve().parent
        / "icon.ico"
    )

    if icon_path.exists():

        app.setWindowIcon(
            QIcon(str(icon_path))
        )

    window = CashBalance()

    window.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    main()