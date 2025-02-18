from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, \
    QGraphicsDropShadowEffect
from PyQt6.uic.properties import QtCore

from Robot import Car
from Connection import Connection
from Joystick import Joystick
from ToSwitch import ToSwitch


class InfoWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Courier New", 17))
        self.setStyleSheet("background-color: #fff; border-radius: 10px; line-height: 100px")
        self.setFixedSize(250, 320)

class Shadow(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__()
        self.setBlurRadius(20)
        self.setXOffset(6)
        self.setYOffset(6)
        self.setColor(QColor("#79A0C1"))

class Wheel_Speed(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        ff = QFont("Courier New", 15)
        # ff.setBold(True)
        self.setFixedSize(310, 330)
        self.fl = QLabel()
        self.fr = QLabel()
        self.bl = QLabel()
        self.br = QLabel()
        self.fl.setText("Front left wheel speed: ")
        self.fl.setFont(ff)
        self.fl.setStyleSheet("color: black")
        self.fr.setText("Front right wheel speed: ")
        self.fr.setFont(ff)
        self.fr.setStyleSheet("color: black")
        self.bl.setText("Back left wheel speed: ")
        self.bl.setFont(ff)
        self.bl.setStyleSheet("color: black")
        self.br.setText("Back right wheel speed: ")
        self.br.setFont(ff)
        self.br.setStyleSheet("color: black")
        l = QGridLayout()
        l.addWidget(self.fl)
        l.addWidget(self.fr)
        l.addWidget(self.bl)
        l.addWidget(self.br)
        self.setLayout(l)

if __name__ == '__main__':
    # Основное окно
    app = QApplication([])
    desktop = QGuiApplication.primaryScreen().geometry()
    width = desktop.width()
    height = desktop.height()
    color1 = QColor("#79A0C1")
    color2 = QColor("#ECEEEF")
    # Градиент
    gradient = QLinearGradient(QPointF(0, height), QPointF(width, 0))
    gradient.setColorAt(0, color1)  # Начальный цвет
    gradient.setColorAt(1, color2)  # Конечный цвет
    palette = QPalette()
    palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
    # Главное окно
    mw = QMainWindow()
    mw.setWindowTitle('Wheeled Robot Control')
    mw.showFullScreen()
    mw.setMinimumSize(width, height)
    # mw.setStyleSheet("background: #a0a6af")
    mw.setPalette(palette)

    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)


    # Поле для машинки
    car_container = QWidget()
    car_container.setStyleSheet("background-color: white; border-top: 2px solid #FCFDFD; border-radius: 10px;")
    car_container.setFixedSize(800, 878)
    car_container.setLayout(QGridLayout())
    # Тень
    shadow1 = Shadow() # Semi-transparent black
    car_container.setGraphicsEffect(shadow1)

    car = Car()
    car_container.layout().addWidget(car)


    # ID
    inputId = QLineEdit()
    inputId.setPlaceholderText("Enter IP Raspberry PI")
    inputId.setStyleSheet("border: none; color: white")
    f = QFont("Courier New", 14)
    f.setBold(True)
    inputId.setFont(f)
    inputId.setFixedSize(400, 50)
    # Вторая тень
    shadow2 = QGraphicsDropShadowEffect()
    shadow2.setBlurRadius(15)
    shadow2.setXOffset(3)
    shadow2.setYOffset(3)
    shadow2.setColor(QColor("#734A12"))  # Semi-transparent black
    # Кнопка подключения
    button_connection = QPushButton("CONNECT")
    font = QFont("Courier New", 14)
    font.setBold(True)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
    button_connection.setFont(font)
    button_connection.setFixedSize(100, 50)
    button_connection.setStyleSheet("background-color: #fde869; text-align: center; color: #734A12")
    button_connection.setGraphicsEffect(shadow2)
    # Первый ярус
    label_container = QWidget()
    label_container.setFixedSize(575, 75)
    label_container.setStyleSheet("background-color: #8ab0c6; border-radius: 10px;")
    shadow3 = Shadow()
    label_container.setGraphicsEffect(shadow3)
    mn = QGridLayout()
    mn.addWidget(inputId, 0, 0, 1, 1)
    mn.addWidget(button_connection, 0, 2, 1, 1)
    label_container.setLayout(mn)


    # Второй ярус - поле подключилось/ошибка подключения
    label_connection = QLabel()
    f2 = QFont("Courier New", 16)
    f2.setBold(True)
    label_connection.setFont(f2)
    label_connection.setStyleSheet("color: #F0F0F0; padding: 2px 2px 2px 10px; letter-spacing: 2px")
    label_connection.setText("Connection is expected")
    label_connection.setFixedSize(580, 40)
    l_c = QWidget()
    l_c.setStyleSheet("background-color: #a4c1ce; border-radius: 10px;")
    l_c.setLayout(QGridLayout())
    l_c.layout().addWidget(label_connection)
    shadow4 = Shadow()
    l_c.setGraphicsEffect(shadow4)
    # label_connection.setStyleSheet("border: 1px solid black")


    # Третий ярус
    label1 = InfoWindow()
    label2 = Wheel_Speed()
    field = QWidget()
    field.setFixedSize(580, 350)
    shadow5 = Shadow()
    field.setGraphicsEffect(shadow5)
    field.setStyleSheet("background-color: #CBDBE1; border: 2px ridge white; border-radius: 10px;")
    k = QGridLayout()
    k.addWidget(label1, 0, 0)
    k.addWidget(label2, 0, 1)
    field.setLayout(k)


    # Соединение ярусов
    # Поле для информации
    information_field = QWidget()
    information_field.setFixedSize(600, 540)
    mm = QGridLayout()
    information_field.setLayout(mm)
    mm.addWidget(label_container, 0, 0, 1, 2)
    mm.addWidget(l_c, 1, 0, 1, 2)
    mm.addWidget(field, 2, 0, 1, 2)


    # Переключатель
    switch = ToSwitch()
    # Режим
    font2 = QFont("Courier New", 18)
    font2.setBold(True)
    font2.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3)
    shadow7 = Shadow()
    shadow7.setXOffset(3)
    shadow7.setYOffset(3)
    label_mode = QLabel()
    label_mode.setGraphicsEffect(shadow7)
    label_mode.setFont(font2)
    label_mode.setText("Rotate mode")
    label_mode.setStyleSheet("color: white")
    label_mode.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # label_mode.setFixedSize(680, 120)
    # label_mode.setStyleSheet("border: 1px solid black; background-color: white;")
    # Поле для свича
    switch_container = QWidget()
    switch_container.setFixedSize(200, 100)
    switch_container.setLayout(QGridLayout())
    switch_container.layout().addWidget(label_mode)
    switch_container.layout().addWidget(switch)


    joystick = Joystick(label1, car, switch)
    shadow6 = Shadow()
    joystick.setGraphicsEffect(shadow6)
    switch.valueChanged.connect(joystick.switch_change)

    connect = Connection(inputId, label_connection, label2, button_connection, joystick)





    # порт и кнопка
    ml.addWidget(car_container, 0, 0, 10, 5)
    ml.addWidget(information_field, 0, 5, 5, 5)

    # нижняя часть
    ml.addWidget(switch_container, 7, 6, 1, 1)
    ml.addWidget(joystick, 6, 7, 5, 3)

    ## Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec()