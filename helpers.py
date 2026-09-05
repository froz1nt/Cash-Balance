from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from config import (
    CARD,
    TEXT,
    BLUE,
    BLUE_HOVER,
    WHITE
)


# ============================================================
# ЧИСЛО
# ============================================================

def number(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


# ============================================================
# ФОРМАТ ЧИСЛА
# ============================================================

def format_number(value):
    value = number(value)

    if value.is_integer():
        return str(int(value))

    return f"{value:.2f}".rstrip(
        "0"
    ).rstrip(".")


# ============================================================
# ДЕНЬГИ
# ============================================================

def money(value):
    return f"${value:,.0f}"
    value = number(value)

    text = f"{value:,.2f}"

    text = text.replace(
        ",",
        " "
    )

    return f"{text} $"


# ============================================================
# СООБЩЕНИЕ
# ============================================================

def show_message(
    parent,
    title,
    text
):
    box = QMessageBox(parent)

    box.setWindowTitle(title)
    box.setText(text)

    box.setIcon(
        QMessageBox.Icon.Information
    )

    box.setStandardButtons(
        QMessageBox.StandardButton.Ok
    )

    box.setStyleSheet(
        f"""
        QMessageBox {{
            background: {CARD};
            color: {TEXT};
        }}

        QMessageBox QLabel {{
            color: {TEXT};
            background: transparent;
            border: none;
        }}

        QMessageBox QPushButton {{
            background: {BLUE};
            color: {WHITE};
            border: none;
            border-radius: 7px;
            min-width: 80px;
            min-height: 32px;
            padding: 0 12px;
        }}

        QMessageBox QPushButton:hover {{
            background: {BLUE_HOVER};
        }}
        """
    )

    box.exec()


# ============================================================
# ОШИБКА
# ============================================================

def show_error(
    parent,
    text
):
    box = QMessageBox(parent)

    box.setWindowTitle(
        "Ошибка"
    )

    box.setText(text)

    box.setIcon(
        QMessageBox.Icon.Warning
    )

    box.setStandardButtons(
        QMessageBox.StandardButton.Ok
    )

    box.setStyleSheet(
        f"""
        QMessageBox {{
            background: {CARD};
            color: {TEXT};
        }}

        QMessageBox QLabel {{
            color: {TEXT};
            background: transparent;
            border: none;
        }}

        QMessageBox QPushButton {{
            background: {BLUE};
            color: {WHITE};
            border: none;
            border-radius: 7px;
            min-width: 80px;
            min-height: 32px;
        }}

        QMessageBox QPushButton:hover {{
            background: {BLUE_HOVER};
        }}
        """
    )

    box.exec()