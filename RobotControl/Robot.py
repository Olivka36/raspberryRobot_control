import math

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QWidget


class Car(QWidget):
    def __init__(self):
        super().__init__()
        self.height = 878
        self.width = 800
        self.car_width = 100
        self.car_height = 150
        self.car_x = 275
        self.car_y = 340
        self.rotation_angle = 0
        self.car_image = QPixmap("car.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        transform = QTransform()

        transform.translate(self.car_x + self.car_width/2, self.car_y + self.car_height/2)
        transform.rotate(self.rotation_angle)
        transform.translate(- self.car_x - self.car_width/2, - self.car_y - self.car_width/2)

        painter.setTransform(transform)
        painter.drawPixmap(int(self.car_x), int(self.car_y), int(self.car_width), int(self.car_height), self.car_image)

        painter.end()

    def move_car(self, direction, speed, flag):
        radians = math.radians(self.rotation_angle)
        if radians >= 2*math.pi or radians <= -2*math.pi:
            self.rotation_angle = 0
            radians = 0
        speed /= 15

        if flag == 0:
            if direction == "Moves Forward":
                self.car_x += speed * math.sin(radians)
                self.car_y -= speed * math.cos(radians)
            elif direction == "Moves Backward":
                self.car_x -= speed * math.sin(radians)
                self.car_y += speed * math.cos(radians)
            elif direction == "Moves Left":
                self.car_y -= speed * math.sin(radians)
                self.car_x -= speed * math.cos(radians)
            elif direction == "Moves Right":
                self.car_y += speed * math.sin(radians)
                self.car_x += speed * math.cos(radians)
        else:
            if direction == "Moves Forward":
                self.car_x += speed * math.sin(radians)
                self.car_y -= speed * math.cos(radians)
            elif direction == "Moves Backward":
                self.car_x -= speed * math.sin(radians)
                self.car_y += speed * math.cos(radians)
            elif direction == "Left Rotation":
                self.rotation_angle -= speed/2
            elif direction == "Right Rotation":
                self.rotation_angle += speed / 2

        self.wrap_position(radians, direction)


    def wrap_position(self, radians, direction):
        x = self.car_x
        y = self.car_y
        pi = math.pi
        c_w = self.car_width
        c_h = self.car_height
        w = self.width
        h = self.height

        if direction == "Moves Right" or direction == "Moves Left":
            if radians < 0:
                phi = math.tan(radians + pi / 2)
            else:
                phi = math.tan(radians - pi / 2)
        else:
            phi = math.tan(radians)

        if phi > 70 or phi < -70:
            phi = 0

        if phi == 0:
            f = 0
        else:
            f = 1/phi

        # if direction == "Moves Forward" or "Moves Backward":
        if y + c_h < 0:
            if -pi/2 <= radians < 0 or pi/2 <= radians < pi or -pi*3/2 <= radians < -pi or pi*3/2 <= radians < pi*2:
                self.car_y += (w - x) * (-f)
                if self.car_y > h or (self.car_y + c_h) < -1:
                    self.car_y = h
                self.car_x -= phi * (self.car_y + c_h)
            else:
                self.car_y += (x + c_w) * f
                if self.car_y > h or (self.car_y + c_h) < -1:
                    self.car_y = h
                self.car_x -= phi * (self.car_y + c_h)

        elif y > h:
            if -pi/2 <= radians < 0 or pi/2 <= radians < pi or -pi*3/2 <= radians < -pi or pi*3/2 <= radians < pi*2:
                self.car_y = h + x * f
                if self.car_y < -1 or self.car_y >= h:
                    self.car_y = 0 - c_h - 1
                self.car_x += phi * (h - self.car_y)
            else:
                self.car_y = h - (w - x) * f
                if self.car_y < 0 or self.car_y >= h:
                    self.car_y = 0 - c_h - 1
                self.car_x += phi * (h + c_h)

        if x + c_w < 0:
            if -pi/2 <= radians < 0 or pi/2 <= radians < pi or -pi*3/2 <= radians < -pi or pi*3/2 <= radians < pi*2:
                self.car_x -= phi * (h - y)
                if self.car_x > w or (self.car_x + c_w) < -1:
                    self.car_x = w
                self.car_y -= (self.car_x + c_w) * f
            else:
                self.car_x += (y + c_h) * phi
                if self.car_x > w or (self.car_x + c_w) < -1:
                    self.car_x = w
                self.car_y -= f * (self.car_x + c_w)

        elif x > w:
            if -pi/2 <= radians < 0 or pi/2 <= radians < pi or -pi*3/2 <= radians < -pi or pi*3/2 <= radians < pi*2:
                self.car_x = w + y * phi
                if self.car_x < -1 or self.car_x >= w:
                    self.car_x = 0 - c_w
                self.car_y += f * (w - self.car_x)
            else:
                self.car_x = w - (h - y) * phi
                if self.car_x < 0 or self.car_x >= w:
                    self.car_x = 0 - c_w - 1
                self.car_y += f * (w + c_w)

        self.update()