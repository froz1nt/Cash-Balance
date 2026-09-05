from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QLinearGradient
)

from PySide6.QtWidgets import QLabel


class GradientLogo(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(
            300,
            42
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        font = QFont(
            "Segoe UI",
            19,
            QFont.Weight.Bold
        )

        gradient = QLinearGradient(
            0,
            0,
            300,
            0
        )

        gradient.setColorAt(
            0.0,
            QColor("#1683ff")
        )

        gradient.setColorAt(
            0.5,
            QColor("#6a8cff")
        )

        gradient.setColorAt(
            1.0,
            QColor("#27d17f")
        )

        path = QPainterPath()

        path.addText(
            0,
            29,
            font,
            "CASH BALANCE"
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            gradient
        )

        painter.drawPath(path)

        painter.end()