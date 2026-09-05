import os
import sys

from pathlib import Path

from PySide6.QtCore import (
    QTimer,
    QPropertyAnimation,
    QEasingCurve
)

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsOpacityEffect
)

from config import (
    BLUE,
    BLUE_HOVER,
    CARD_2,
    CARD_3
)

from styles import (
    application_style,
    button_style,
    input_style
)

from widgets import (
    AnimatedButton,
    GradientLogo
)

from storage import (
    load_data,
    save_data
)

from app.helpers import (
    number,
    money
)

from app import history
from app import create_page


class CashBalance(QWidget):

    # ========================================================
    # ИНИЦИАЛИЗАЦИЯ
    # ========================================================

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Cash Balance"
        )

        self.resize(
            1150,
            750
        )

        self.setMinimumSize(
            950,
            650
        )

        self.operations = []
        self.goal = None

        self.operation_type = "Доход"

        self.current_page = None

        self._page_animation = None

        self.setup_icon()

        self.setup_style()

        self.load_data()

        self.main = QVBoxLayout(self)

        self.main.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.main.setSpacing(0)

        self.show_history()

        self.save_timer = QTimer(self)

        self.save_timer.timeout.connect(
            self.auto_save
        )

        self.save_timer.start(2000)

    # ========================================================
    # ИКОНКА
    # ========================================================

    def setup_icon(self):

        # icon.ico лежит в корне проекта,
        # рядом с main.py

        icon_path = (
            Path(__file__).resolve().parent.parent
            / "icon.ico"
        )

        if icon_path.exists():

            self.setWindowIcon(
                QIcon(str(icon_path))
            )

    # ========================================================
    # СТИЛИ
    # ========================================================

    def setup_style(self):

        self.setStyleSheet(
            application_style()
        )

    # ========================================================
    # АНИМАЦИЯ СТРАНИЦЫ
    # ========================================================

    def animate_page(
        self,
        widget
    ):
        try:

            effect = QGraphicsOpacityEffect(
                widget
            )

            effect.setOpacity(0.0)

            widget.setGraphicsEffect(
                effect
            )

            animation = QPropertyAnimation(
                effect,
                b"opacity",
                self
            )

            animation.setDuration(180)

            animation.setStartValue(0.0)

            animation.setEndValue(1.0)

            animation.setEasingCurve(
                QEasingCurve.Type.OutCubic
            )

            self._page_animation = animation

            def finish():

                try:
                    widget.setGraphicsEffect(
                        None
                    )

                except Exception:
                    pass

            animation.finished.connect(
                finish
            )

            animation.start()

        except Exception:

            try:
                widget.setGraphicsEffect(
                    None
                )

            except Exception:
                pass

    # ========================================================
    # СОХРАНЕНИЕ
    # ========================================================

    def save_data(self):

        save_data(
            self.operations,
            self.goal
        )

    # ========================================================
    # ЗАГРУЗКА
    # ========================================================

    def load_data(self):

        (
            self.operations,
            self.goal
        ) = load_data()

    # ========================================================
    # АВТОСОХРАНЕНИЕ
    # ========================================================

    def auto_save(self):

        self.save_data()

    # ========================================================
    # ЗАКРЫТИЕ
    # ========================================================

    def closeEvent(
        self,
        event
    ):
        self.save_data()

        event.accept()

    # ========================================================
    # ОБЩАЯ КНОПКА
    # ========================================================

    def button(
        self,
        text,
        callback=None,
        bg=BLUE,
        hover=BLUE_HOVER,
        height=42,
        width=None
    ):

        btn = AnimatedButton(text)

        btn.setFixedHeight(
            height
        )

        if width:
            btn.setFixedWidth(
                width
            )

        btn.setStyleSheet(
            button_style(
                bg,
                hover
            )
        )

        if callback:

            btn.clicked.connect(
                callback
            )

        return btn

    # ========================================================
    # ОЧИСТКА СТРАНИЦЫ
    # ========================================================

    def clear_page(self):

        while self.main.count():

            item = self.main.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    # ========================================================
    # ОБЁРТКА
    # ========================================================

    def page_wrapper(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            36,
            28,
            36,
            30
        )

        layout.setSpacing(0)

        return page, layout

    # ========================================================
    # ЛОГОТИП
    # ========================================================

    def logo(self):

        return GradientLogo()

    # ========================================================
    # СТРАНИЦА ИСТОРИИ
    # ========================================================

    def show_history(self):

        history.show_history(self)

    # ========================================================
    # СТРАНИЦА СОЗДАНИЯ
    # ========================================================

    def show_create_page(self):

        create_page.show_create_page(self)

    # ========================================================
    # ТИП ОПЕРАЦИИ
    # ========================================================

    def set_operation_type(
        self,
        operation_type,
        update_callback
    ):

        create_page.set_operation_type(
            self,
            operation_type,
            update_callback
        )

    # ========================================================
    # LABEL ПОЛЯ
    # ========================================================

    def field_label(
        self,
        text
    ):

        return create_page.field_label(
            self,
            text
        )

    # ========================================================
    # INPUT
    # ========================================================

    def fixed_input(
        self,
        placeholder
    ):

        return create_page.fixed_input(
            self,
            placeholder
        )

    # ========================================================
    # СОЗДАНИЕ ОПЕРАЦИИ
    # ========================================================

    def create_operation(
        self,
        price_entry,
        quantity_entry,
        comment_entry
    ):

        create_page.create_operation(
            self,
            price_entry,
            quantity_entry,
            comment_entry
        )

    # ========================================================
    # ЦЕЛЬ
    # ========================================================

    def save_goal(
        self,
        entry
    ):

        create_page.save_goal(
            self,
            entry
        )

    # ========================================================
    # УДАЛЕНИЕ
    # ========================================================

    def delete_transaction(
        self,
        operation
    ):

        try:

            self.operations.remove(
                operation
            )

        except ValueError:

            return

        self.save_data()

        self.show_history()

    # ========================================================
    # БАЛАНС
    # ========================================================

    def calculate_balance(self):

        balance = 0.0

        for operation in self.operations:

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

            if operation.get(
                "type"
            ) == "Доход":

                balance += total

            else:

                balance -= total

        return balance

    # ========================================================
    # ЗНАЧЕНИЕ ЦЕЛИ
    # ========================================================

    def goal_value(self):

        if self.goal is None:

            return 0

        return max(
            self.goal - self.calculate_balance(),
            0
        )

    # ========================================================
    # ЧИСЛО
    # ========================================================

    def number(
        self,
        value
    ):

        return number(value)

    # ========================================================
    # ФОРМАТ ЧИСЛА
    # ========================================================

    def format_number(
        self,
        value
    ):

        from app.helpers import format_number

        return format_number(value)

    # ========================================================
    # ДЕНЬГИ
    # ========================================================

    def money(
        self,
        value
    ):

        return money(value)

    # ========================================================
    # LIGHTEN
    # ========================================================

    def lighten(
        self,
        color
    ):

        from PySide6.QtGui import QColor

        try:

            qcolor = QColor(color)

            if not qcolor.isValid():

                return color

            qcolor = qcolor.lighter(115)

            return qcolor.name()

        except Exception:

            return color