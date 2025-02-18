from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class ToSwitch(QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setRange(0, 1)
        self.setPageStep(1)
        self.setFixedHeight(50)
        self.setFixedWidth(100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рисуем фон
        bg_color = QColor("#FFF0A3") if self.value() == 0 else QColor("#fbc21d")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        # Рисуем переключатель
        knob_color = QColor("#fff")
        painter.setBrush(QBrush(knob_color))
        painter.setPen(QPen(QColor("#edb32e"), 2.6))
        knob_x = 0 if self.value() == 0 else self.width() - self.height()
        painter.drawRoundedRect(knob_x, 0, self.height(), self.height(), 20, 20)