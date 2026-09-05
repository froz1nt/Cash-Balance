from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)

from config import (
    CARD,
    CARD_2,
    CARD_3,
    WHITE,
    TEXT,
    MUTED,
    GREEN,
    RED,
    BLUE,
    BLUE_HOVER
)

from widgets import RoundedFrame

from styles import input_style, tab_style

from app.helpers import (
    show_message,
    show_error
)

from datetime import datetime


# ============================================================
# СТРАНИЦА СОЗДАНИЯ
# ============================================================

def show_create_page(self):

    self.clear_page()

    page, layout = self.page_wrapper()

    # --------------------------------------------------------
    # Верх
    # --------------------------------------------------------

    top = QHBoxLayout()

    back_btn = self.button(
        "← Назад",
        self.show_history,
        CARD_2,
        CARD_3,
        40
    )

    top.addWidget(back_btn)
    top.addStretch()

    layout.addLayout(top)

    layout.addSpacing(24)

    # --------------------------------------------------------
    # Заголовок
    # --------------------------------------------------------

    title = QLabel(
        "Создать операцию"
    )

    title.setStyleSheet(
        f"""
        QLabel {{
            color: {WHITE};
            font-size: 27px;
            font-weight: 700;
            background: transparent;
            border: none;
        }}
        """
    )

    layout.addWidget(title)

    subtitle = QLabel(
        "Добавьте доход или расход"
    )

    subtitle.setStyleSheet(
        f"""
        QLabel {{
            color: {MUTED};
            font-size: 13px;
            background: transparent;
            border: none;
        }}
        """
    )

    layout.addWidget(subtitle)

    layout.addSpacing(25)

    # --------------------------------------------------------
    # Центральная карточка
    # --------------------------------------------------------

    card = RoundedFrame(CARD)

    card_layout = QVBoxLayout(card)

    card_layout.setContentsMargins(
        28,
        26,
        28,
        28
    )

    card_layout.setSpacing(18)

    # --------------------------------------------------------
    # Доход / Расход
    # --------------------------------------------------------

    tabs = QHBoxLayout()

    tabs.setSpacing(8)

    income_btn = QPushButton(
        "Доход"
    )

    expense_btn = QPushButton(
        "Расход"
    )

    income_btn.setFixedHeight(42)
    expense_btn.setFixedHeight(42)

    income_btn.setFocusPolicy(
        Qt.FocusPolicy.NoFocus
    )

    expense_btn.setFocusPolicy(
        Qt.FocusPolicy.NoFocus
    )

    income_btn.setAutoDefault(False)
    expense_btn.setAutoDefault(False)

    def update_tabs():

        if self.operation_type == "Доход":

            income_btn.setStyleSheet(
                tab_style(GREEN)
            )

            expense_btn.setStyleSheet(
                tab_style(CARD_2)
            )

        else:

            income_btn.setStyleSheet(
                tab_style(CARD_2)
            )

            expense_btn.setStyleSheet(
                tab_style(RED)
            )

    income_btn.clicked.connect(
        lambda:
        self.set_operation_type(
            "Доход",
            update_tabs
        )
    )

    expense_btn.clicked.connect(
        lambda:
        self.set_operation_type(
            "Расход",
            update_tabs
        )
    )

    update_tabs()

    tabs.addWidget(income_btn)
    tabs.addWidget(expense_btn)

    card_layout.addLayout(tabs)

    # --------------------------------------------------------
    # Поля
    # --------------------------------------------------------

    form = QGridLayout()

    form.setHorizontalSpacing(16)
    form.setVerticalSpacing(13)

    price_label = self.field_label(
        "Цена"
    )

    quantity_label = self.field_label(
        "Количество"
    )

    comment_label = self.field_label(
        "Комментарий"
    )

    goal_label = self.field_label(
        "Цель"
    )

    price_entry = self.fixed_input(
        "Введите цену"
    )

    quantity_entry = self.fixed_input(
        "Введите количество"
    )

    comment_entry = QLineEdit()

    comment_entry.setPlaceholderText(
        "Комментарий"
    )

    comment_entry.setMaxLength(35)

    comment_entry.setFixedHeight(46)

    comment_entry.setStyleSheet(
        input_style()
    )

    goal_entry = self.fixed_input(
        "Введите цель"
    )

    form.addWidget(
        price_label,
        0,
        0
    )

    form.addWidget(
        quantity_label,
        0,
        1
    )

    form.addWidget(
        price_entry,
        1,
        0
    )

    form.addWidget(
        quantity_entry,
        1,
        1
    )

    form.addWidget(
        comment_label,
        2,
        0,
        1,
        2
    )

    form.addWidget(
        comment_entry,
        3,
        0,
        1,
        2
    )

    form.addWidget(
        goal_label,
        4,
        0,
        1,
        2
    )

    form.addWidget(
        goal_entry,
        5,
        0,
        1,
        2
    )

    card_layout.addLayout(form)

    card_layout.addSpacing(5)

    # --------------------------------------------------------
    # Сохранение цели
    # --------------------------------------------------------

    save_goal_btn = self.button(
        "Сохранить цель",
        lambda:
        self.save_goal(goal_entry),
        CARD_2,
        CARD_3,
        40
    )

    card_layout.addWidget(
        save_goal_btn,
        alignment=Qt.AlignmentFlag.AlignLeft
    )

    card_layout.addSpacing(5)

    # --------------------------------------------------------
    # Создание
    # --------------------------------------------------------

    create_btn = self.button(
        "Создать операцию",
        lambda:
        self.create_operation(
            price_entry,
            quantity_entry,
            comment_entry
        ),
        BLUE,
        BLUE_HOVER,
        46
    )

    card_layout.addWidget(
        create_btn
    )

    layout.addWidget(card)

    layout.addStretch()

    self.main.addWidget(page)

    self.animate_page(page)


# ============================================================
# ТИП ОПЕРАЦИИ
# ============================================================

def set_operation_type(
    self,
    operation_type,
    update_callback
):
    self.operation_type = operation_type

    update_callback()


# ============================================================
# LABEL ПОЛЯ
# ============================================================

def field_label(
    self,
    text
):
    label = QLabel(text)

    label.setStyleSheet(
        f"""
        QLabel {{
            color: {TEXT};
            font-size: 13px;
            font-weight: 600;
            background: transparent;
            border: none;
        }}
        """
    )

    return label


# ============================================================
# INPUT
# ============================================================

def fixed_input(
    self,
    placeholder
):
    entry = QLineEdit()

    entry.setPlaceholderText(
        placeholder
    )

    entry.setFixedHeight(46)

    entry.setMinimumWidth(180)

    entry.setStyleSheet(
        input_style()
    )

    return entry


# ============================================================
# СОЗДАНИЕ ОПЕРАЦИИ
# ============================================================

def create_operation(
    self,
    price_entry,
    quantity_entry,
    comment_entry
):
    price_text = price_entry.text().strip()

    quantity_text = quantity_entry.text().strip()

    comment = comment_entry.text().strip()

    comment = comment[:35]

    if not price_text:
        show_error(
            self,
            "Введите цену."
        )
        return

    try:
        price = float(
            price_text.replace(",", ".")
        )

    except ValueError:
        show_error(
            self,
            "Цена должна быть числом."
        )
        return

    if price < 0:
        show_error(
            self,
            "Цена не может быть отрицательной."
        )
        return

    if quantity_text:

        try:
            quantity = float(
                quantity_text.replace(
                    ",",
                    "."
                )
            )

        except ValueError:
            show_error(
                self,
                "Количество должно быть числом."
            )
            return

    else:
        quantity = 1

    if quantity <= 0:
        show_error(
            self,
            "Количество должно быть больше нуля."
        )
        return

    operation = {
        "id": datetime.now().timestamp(),
        "type": self.operation_type,
        "price": price,
        "quantity": quantity,
        "comment": comment,
        "date": datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        )
    }

    self.operations.append(
        operation
    )

    self.save_data()

    self.show_history()


# ============================================================
# СОХРАНЕНИЕ ЦЕЛИ
# ============================================================

def save_goal(
    self,
    entry
):
    value = entry.text().strip()

    if not value:

        self.goal = None

        self.save_data()

        show_message(
            self,
            "Цель",
            "Цель сброшена."
        )

        return

    try:
        goal = float(
            value.replace(",", ".")
        )

    except ValueError:

        show_error(
            self,
            "Цель должна быть числом."
        )

        return

    if goal <= 0:

        show_error(
            self,
            "Цель должна быть больше нуля."
        )

        return

    self.goal = goal

    self.save_data()

    show_message(
        self,
        "Цель",
        "Цель сохранена."
    )