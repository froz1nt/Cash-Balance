from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QScrollArea
)

from config import (
    CARD,
    CARD_2,
    CARD_3,
    BLUE,
    BLUE_HOVER,
    WHITE,
    TEXT,
    MUTED,
    GREEN,
    RED,
    BORDER,
    BORDER_LIGHT,
)

from widgets import (
    AnimatedButton,
    RoundedFrame
)

from app.helpers import (
    number,
    format_number,
    money
)


# ============================================================
# ИСТОРИЯ
# ============================================================

def show_history(self):
    self.clear_page()

    page, layout = self.page_wrapper()

    # --------------------------------------------------------
    # Верхняя панель
    # --------------------------------------------------------

    top = QHBoxLayout()

    top.setContentsMargins(
        0,
        0,
        0,
        0
    )

    logo = self.logo()

    top.addWidget(logo)
    top.addStretch()

    create_btn = self.button(
        "Создать операцию",
        self.show_create_page,
        BLUE,
        BLUE_HOVER,
        44
    )

    top.addWidget(create_btn)

    layout.addLayout(top)

    layout.addSpacing(30)

    # --------------------------------------------------------
    # Статистика
    # --------------------------------------------------------

    stats = QHBoxLayout()
    stats.setSpacing(14)

    balance = self.calculate_balance()

    balance_card = stat_card(
        self,
        "Баланс",
        money(balance),
        BLUE
    )

    goal_value = self.goal_value()

    if self.goal is None:
        goal_text = "—"
    else:
        goal_text = money(
            max(self.goal - balance, 0)
        )

    goal_card = stat_card(
        self,
        "До цели",
        goal_text,
        GREEN
    )

    if self.goal is None:
        target_text = "Не задана"
    else:
        target_text = money(self.goal)

    target_card = stat_card(
        self,
        "Цель",
        target_text,
        WHITE
    )

    stats.addWidget(balance_card)
    stats.addWidget(goal_card)
    stats.addWidget(target_card)

    layout.addLayout(stats)

    layout.addSpacing(22)

    # --------------------------------------------------------
    # История
    # --------------------------------------------------------

    history_card = RoundedFrame(CARD)

    history_layout = QVBoxLayout(
        history_card
    )

    history_layout.setContentsMargins(
        22,
        20,
        22,
        20
    )

    history_layout.setSpacing(12)

    history_title = QLabel(
        "История"
    )

    history_title.setStyleSheet(
        f"""
        QLabel {{
            color: {WHITE};
            font-size: 18px;
            font-weight: 700;
            background: transparent;
            border: none;
        }}
        """
    )

    history_layout.addWidget(
        history_title
    )

    scroll = QScrollArea()

    scroll.setWidgetResizable(True)
    scroll.setFrameShape(
        QFrame.Shape.NoFrame
    )

    content = QWidget()

    content_layout = QVBoxLayout(
        content
    )

    content_layout.setContentsMargins(
        0,
        4,
        0,
        4
    )

    content_layout.setSpacing(0)

    if not self.operations:

        empty = QLabel(
            "Операций пока нет"
        )

        empty.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        empty.setMinimumHeight(180)

        empty.setStyleSheet(
            f"""
            QLabel {{
                color: {MUTED};
                font-size: 14px;
                background: transparent;
                border: none;
            }}
            """
        )

        content_layout.addWidget(
            empty
        )

    else:

        add_history_header(
            self,
            content_layout
        )

        for operation in reversed(
            self.operations
        ):
            row = transaction_row(
                self,
                operation
            )

            content_layout.addWidget(row)

    content_layout.addStretch()

    scroll.setWidget(content)

    history_layout.addWidget(scroll)

    layout.addWidget(
        history_card,
        1
    )

    self.main.addWidget(page)

    self.animate_page(page)


# ============================================================
# СТАТИСТИКА
# ============================================================

def stat_card(
    self,
    title,
    value,
    accent
):
    card = RoundedFrame(CARD)

    card.setMinimumHeight(105)

    layout = QVBoxLayout(card)

    layout.setContentsMargins(
        20,
        17,
        20,
        17
    )

    layout.setSpacing(7)

    title_label = QLabel(title)

    title_label.setStyleSheet(
        f"""
        QLabel {{
            color: {MUTED};
            font-size: 13px;
            background: transparent;
            border: none;
        }}
        """
    )

    value_label = QLabel(value)

    value_label.setStyleSheet(
        f"""
        QLabel {{
            color: {accent};
            font-size: 25px;
            font-weight: 700;
            background: transparent;
            border: none;
        }}
        """
    )

    layout.addWidget(title_label)
    layout.addWidget(value_label)

    return card


# ============================================================
# ШАПКА ИСТОРИИ
# ============================================================

def add_history_header(
    self,
    layout
):
    row = QFrame()

    row.setFixedHeight(36)

    grid = QGridLayout(row)

    grid.setContentsMargins(
        12,
        0,
        12,
        0
    )

    grid.setHorizontalSpacing(8)

    headers = [
        ("Тип", 0),
        ("Цена", 1),
        ("Кол-во", 2),
        ("Сумма", 3),
        ("Комментарий", 4),
        ("Дата", 5),
        ("", 6)
    ]

    for text, column in headers:

        label = QLabel(text)

        label.setStyleSheet(
            f"""
            QLabel {{
                color: {MUTED};
                font-size: 11px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
            """
        )

        grid.addWidget(
            label,
            0,
            column
        )

    set_history_columns(grid)

    layout.addWidget(row)


# ============================================================
# КОЛОНКИ
# ============================================================

def set_history_columns(grid):

    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)
    grid.setColumnStretch(2, 1)
    grid.setColumnStretch(3, 1)
    grid.setColumnStretch(4, 2)
    grid.setColumnStretch(5, 2)

    grid.setColumnMinimumWidth(
        6,
        35
    )


# ============================================================
# СТРОКА
# ============================================================

def transaction_row(
    self,
    operation
):
    row = QFrame()

    row.setMinimumHeight(55)

    row.setStyleSheet(
        f"""
        QFrame {{
            background: {CARD};
            border: none;
            border-radius: 0px;
        }}

        QFrame:hover {{
            background: {CARD_2};
        }}
        """
    )

    grid = QGridLayout(row)

    grid.setContentsMargins(
        12,
        6,
        4,
        6
    )

    grid.setHorizontalSpacing(8)

    operation_type = operation.get(
        "type",
        "Доход"
    )

    price = number(
        operation.get(
            "price",
            0
        )
    )

    quantity = number(
        operation.get(
            "quantity",
            1
        )
    )

    total = price * quantity

    comment = str(
        operation.get(
            "comment",
            ""
        )
    )[:35]

    date = str(
        operation.get(
            "date",
            ""
        )
    )

    type_label = QLabel(
        operation_type
    )

    type_color = (
        GREEN
        if operation_type == "Доход"
        else RED
    )

    type_label.setStyleSheet(
        f"""
        QLabel {{
            color: {type_color};
            font-size: 12px;
            font-weight: 700;
            background: transparent;
            border: none;
        }}
        """
    )

    price_label = row_label(
        self,
        money(price)
    )

    quantity_label = row_label(
        self,
        format_number(quantity)
    )

    total_label = row_label(
        self,
        money(total)
    )

    comment_label = row_label(
        self,
        comment if comment else "—"
    )

    comment_label.setToolTip(
        comment
    )

    date_label = row_label(
        self,
        date
    )

    delete_btn = AnimatedButton(
        "✕"
    )

    delete_btn.setFixedSize(
        30,
        30
    )

    delete_btn.setFocusPolicy(
        Qt.FocusPolicy.NoFocus
    )

    delete_btn.setAutoDefault(False)

    delete_btn.setStyleSheet(
        f"""
        QPushButton {{
            background: transparent;
            color: {MUTED};
            border: none;
            outline: none;
            font-size: 14px;
            font-weight: 600;
        }}

        QPushButton:hover {{
            background: transparent;
            color: {RED};
            border: none;
            outline: none;
        }}

        QPushButton:pressed {{
            background: transparent;
            color: #d93647;
            border: none;
            outline: none;
        }}

        QPushButton:focus {{
            background: transparent;
            color: {MUTED};
            border: none;
            outline: none;
        }}
        """
    )

    delete_btn.clicked.connect(
        lambda checked=False,
        op=operation:
        self.delete_transaction(op)
    )

    grid.addWidget(
        type_label,
        0,
        0
    )

    grid.addWidget(
        price_label,
        0,
        1
    )

    grid.addWidget(
        quantity_label,
        0,
        2
    )

    grid.addWidget(
        total_label,
        0,
        3
    )

    grid.addWidget(
        comment_label,
        0,
        4
    )

    grid.addWidget(
        date_label,
        0,
        5
    )

    grid.addWidget(
        delete_btn,
        0,
        6
    )

    set_history_columns(grid)

    return row


# ============================================================
# LABEL СТРОКИ
# ============================================================

def row_label(
    self,
    text
):
    label = QLabel(
        str(text)
    )

    label.setStyleSheet(
        f"""
        QLabel {{
            color: {TEXT};
            font-size: 12px;
            background: transparent;
            border: none;
            outline: none;
        }}
        """
    )

    label.setTextInteractionFlags(
        Qt.TextInteractionFlag.NoTextInteraction
    )

    return label