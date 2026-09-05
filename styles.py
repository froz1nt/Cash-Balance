from config import (
    BG,
    CARD,
    CARD_2,
    CARD_3,
    BLUE,
    BLUE_HOVER,
    WHITE,
    TEXT,
    MUTED,
    BORDER,
    BORDER_LIGHT
)


# ============================================================
# ОСНОВНОЙ STYLE SHEET
# ============================================================

def application_style():
    return f"""
        QWidget {{
            background: {BG};
            color: {TEXT};
            font-family: Segoe UI;
        }}

        QFrame {{
            border: none;
        }}

        QLabel {{
            background: transparent;
            border: none;
            outline: none;
        }}

        QPushButton {{
            border: none;
            outline: none;
        }}

        QPushButton:focus {{
            border: none;
            outline: none;
        }}

        QLineEdit {{
            selection-background-color: {BLUE};
            selection-color: {WHITE};
        }}

        QTextEdit {{
            selection-background-color: {BLUE};
            selection-color: {WHITE};
        }}

        QScrollArea {{
            border: none;
            background: transparent;
        }}

        QScrollBar:vertical {{
            background: {CARD};
            width: 7px;
            border: none;
            margin: 4px 0;
        }}

        QScrollBar::handle:vertical {{
            background: {BORDER_LIGHT};
            border-radius: 3px;
            min-height: 35px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {MUTED};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: transparent;
        }}
    """


# ============================================================
# STYLE КНОПКИ
# ============================================================

def button_style(
    bg=BLUE,
    hover=BLUE_HOVER
):
    return f"""
        QPushButton {{
            background: {bg};
            color: {WHITE};
            border: none;
            border-radius: 9px;
            padding: 0 18px;
            font-size: 14px;
            font-weight: 600;
            outline: none;
        }}

        QPushButton:hover {{
            background: {hover};
        }}

        QPushButton:pressed {{
            background: {bg};
        }}

        QPushButton:focus {{
            border: none;
            outline: none;
        }}
    """


# ============================================================
# STYLE ПОЛЯ
# ============================================================

def input_style():
    return f"""
        QLineEdit {{
            background: {CARD_2};
            color: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 9px;
            padding: 0 13px;
            font-size: 13px;
            outline: none;
        }}

        QLineEdit:hover {{
            border: 1px solid {BORDER_LIGHT};
        }}

        QLineEdit:focus {{
            border: 1px solid {BLUE};
            outline: none;
        }}
    """


# ============================================================
# STYLE TAB
# ============================================================

def tab_style(background):
    from PySide6.QtGui import QColor

    try:
        color = QColor(background)

        if color.isValid():
            hover = color.lighter(115).name()
        else:
            hover = background

    except Exception:
        hover = background

    return f"""
        QPushButton {{
            background: {background};
            color: {WHITE};
            border: none;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 600;
            outline: none;
        }}

        QPushButton:hover {{
            background: {hover};
        }}

        QPushButton:focus {{
            border: none;
            outline: none;
        }}
    """