from PySide6.QtWidgets import QFrame

from config import CARD


class RoundedFrame(QFrame):

    def __init__(
        self,
        background=CARD,
        radius=12,
        parent=None
    ):
        super().__init__(parent)

        self.setObjectName(
            "RoundedFrame"
        )

        self.setStyleSheet(
            f"""
            QFrame#RoundedFrame {{
                background: {background};
                border: none;
                border-radius: {radius}px;
            }}
            """
        )