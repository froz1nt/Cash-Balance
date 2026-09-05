from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect


class AnimatedButton(QPushButton):

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAutoDefault(False)

        # Эффект прозрачности
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # Кнопка сразу существует и начинает появляться
        self.opacity_effect.setOpacity(0.0)

        self.appear_animation = QPropertyAnimation(
            self.opacity_effect,
            b"opacity",
            self
        )

        self.appear_animation.setDuration(300)
        self.appear_animation.setStartValue(0.0)
        self.appear_animation.setEndValue(1.0)
        self.appear_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        # Анимация при наведении
        self.hover_animation = QPropertyAnimation(
            self.opacity_effect,
            b"opacity",
            self
        )

        self.hover_animation.setDuration(100)
        self.hover_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        # Запускаем появление сразу
        self.appear_animation.start()

    def enterEvent(self, event):
        self.hover_animation.stop()

        self.hover_animation.setStartValue(
            self.opacity_effect.opacity()
        )

        self.hover_animation.setEndValue(0.86)

        self.hover_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_animation.stop()

        self.hover_animation.setStartValue(
            self.opacity_effect.opacity()
        )

        self.hover_animation.setEndValue(1.0)

        self.hover_animation.start()

        super().leaveEvent(event)