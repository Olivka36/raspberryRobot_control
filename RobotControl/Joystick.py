from PyQt6.QtGui import *
from PyQt6.QtCore import *
import math

from PyQt6.QtWidgets import QWidget


class Joystick(QWidget):
    joystickMoved = pyqtSignal(str, int, int)

    def __init__(self, label=None, car=None, switch=None, parent=None):
        super().__init__()
        self.movingOffset = self._center()
        self.grabCenter = False
        self.mouseRelease = False
        self.switchFlag = 0
        self.__maxDistance = 90
        self.label = label
        self.car = car
        self.switch = switch

        self.timer = QTimer()
        self.timer.timeout.connect(self._moveJoystick)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self._updatePosition)
        self.timer2.start(50)

    def paintEvent(self, event):
        # рисуем кружочек в качестве джойстика
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance *2 , self.__maxDistance *2 ).translated(self._center())
        pen = QPen(QColor("white"), 1)
        painter.setPen(pen)
        gradient = QRadialGradient(self._center()*0.8, self.__maxDistance*1.5)
        gradient.setColorAt(0, QColor("#FFF0A3"))  # Начальный цвет
        gradient.setColorAt(1, QColor("#fbc21d"))  # Конечный цвет
        # определяет границы кружочка
        painter.setBrush(gradient)
        painter.drawEllipse(bounds)
        # рисуем джойстик
        painter.setBrush(QColor("white"))
        painter.drawEllipse(self._centerEllipse())
        # self.moveCar()


    def _centerEllipse(self):
        if self.movingOffset.x() > self._center().x():
            a = (self.movingOffset.x() - self._center().x() + 90) / 90
        else:
            a = (self._center().x() - self.movingOffset.x() + 90) / 90

        if self.movingOffset.y() > self._center().y():
            b = (self.movingOffset.y() - self._center().y() + 90) / 90
        else:
            b = (self._center().y() - self.movingOffset.y() + 90) / 90

        c = a * b
        if c > 2:
            c = 2

        if not self.grabCenter and not self.mouseRelease:
            return QRectF(-15, -15, 30, 30).translated(self._center())
        return QRectF(-15 * c ** 1.5, -15 * c ** 1.5, 30 * c ** 1.5, 30 * c ** 1.5).translated(self.movingOffset)

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def switch_change(self):
        self.switchFlag = self.switch.value()
        # print(self.switchFlag)


    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), QPointF(point))
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def joystickDirection(self):
        if (not self.grabCenter and not self.mouseRelease):
            return ("No movement", 0)
        normVector = QLineF(self._center(), self.movingOffset)
        currentDistance = normVector.length()
        # print(currentDistance, self._center(), self.movingOffset)
        currentDistance = math.ceil(300*currentDistance/90)
        angle = normVector.angle()

        distance = min(currentDistance, 300)
        if self.switchFlag == 0:
            if 45 <= angle < 135:
                return ("Moves Forward", distance)
            elif 135 <= angle < 225:
                return ("Moves Left", distance)
            elif 225 <= angle < 315:
                return ("Moves Backward", distance)
            else:
                return ("Moves Right", distance)
        else:
            if 45 <= angle < 135:
                return ("Moves Forward", distance)
            elif 135 <= angle < 225:
                return ("Left Rotation", distance)
            elif 225 <= angle < 315:
                return ("Moves Backward", distance)
            else:
                return ("Right Rotation", distance)

    def moveCar(self):
        direction, speed = self.joystickDirection()
        self.label.setText(str(direction) + "\n\n Speed: " + str(speed))
        self.car.move_car(direction, speed, self.switchFlag)

    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(QPointF(ev.pos()))
        # direction, speed = self.joystickDirection()
        # self.joystickMoved.emit(direction, speed, self.switchFlag)
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(ev.pos())
            self.mouseRelease = False
            # self.moveCar()
            self.update()
        return super().mousePressEvent(ev)

    def mouseMoveEvent(self, event):
        direction, speed = self.joystickDirection()
        self.joystickMoved.emit(direction, speed, self.switchFlag)
        if self.grabCenter and not self.mouseRelease:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if self.grabCenter:
            self.mouseRelease = True
            self.grabCenter = False
            self.timer.start(70)
            self._moveJoystick()

    def _moveJoystick(self):
        self.moveCar()
        deltax = abs(self._center().x() - self.movingOffset.x()) / 5
        deltay = abs(self._center().y() - self.movingOffset.y()) / 5
        if not self.grabCenter:
            if (deltax < 0.5 and deltay < 0.5):  # Если достигли целевой точки
                self.movingOffset = self._center()
                self.timer.stop()
                self.mouseRelease = False
            else:
                if self._center().x() < self.movingOffset.x():
                    if self._center().y() < self.movingOffset.y():
                        self.movingOffset.setX(self.movingOffset.x() - deltax)
                        self.movingOffset.setY(self.movingOffset.y() - deltay)
                    else:
                        self.movingOffset.setX(self.movingOffset.x() - deltax)
                        self.movingOffset.setY(self.movingOffset.y() + deltay)
                else:
                    if self._center().y() > self.movingOffset.y():
                        self.movingOffset.setX(self.movingOffset.x() + deltax)
                        self.movingOffset.setY(self.movingOffset.y() + deltay)
                    else:
                        self.movingOffset.setX(self.movingOffset.x() + deltax)
                        self.movingOffset.setY(self.movingOffset.y() - deltay)
        direction, speed = self.joystickDirection()
        self.joystickMoved.emit(direction, speed, self.switchFlag)
        self.update()
        return self.movingOffset

    def _updatePosition(self):
        if self.grabCenter or not self.mouseRelease:
            self.moveCar()
