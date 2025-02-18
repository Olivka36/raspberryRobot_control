from PyQt6.QtCore import QTimer, QObject

import socket

class Connection(QObject):
    UDP_IP = "-"  # IP-адрес Raspberry Pi Pico W
    UDP_PORT = 5005
    MESSAGE = ""
    encoder_values = [0, 0, 0, 0]

    def __init__(self, inputID=None, label_connection=None, label2=None, button_connection=None, joystick=None):
        super().__init__()
        self.inputID = inputID
        self.label2 = label2
        self.rotate_mode = joystick.switchFlag
        self.button_connection = button_connection
        self.l_c = label_connection
        self.joystick = joystick

        self.button_connection.clicked.connect(self.setIP)
        if self.joystick:
            # Подключение сигнала к слоту
            self.joystick.joystickMoved.connect(self.send_message)

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.read_udp)

    def read_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if (self.UDP_IP != "-"):
            # try:
            sock.bind(("0.0.0.0", self.UDP_PORT))
            data, addr = sock.recvfrom(255)
            self.encoder_values = self.parse_input_string(data.decode())
            self.l_c.setText("Robot connected")
            print("Data received: %s" % data.decode())
        else:
            print("UDP_UP: %s, waiting for connection..." % self.UDP_IP)

        self.label2.fl.setText("Front left wheel speed: " + str(self.encoder_values[0]))
        self.label2.fr.setText("Front right wheel speed: " + str(self.encoder_values[1]))
        self.label2.bl.setText("Back left wheel speed: " + str(self.encoder_values[2]))
        self.label2.br.setText("Back right wheel speed: " + str(self.encoder_values[3]))
        sock.close()

    def parse_input_string(self, input_string):
        numbers = input_string.split(";")
        numbers_array = []

        for num in numbers:
            try:
                num = float(num)
                if (num > 1000):
                    num = -(65536 - num)
                numbers_array.append(num)
            except ValueError:
                print(f"Невозможно преобразовать '{num}' в число")

        return numbers_array

    def setIP(self):
        ip = self.inputID.text()
        try:
            # Проверка корректности IP-адреса
            socket.inet_aton(ip)
            # Проверка на то, что это не специальный IP-адрес
            if ip.count('.') == 3 and all(0 <= int(num) < 256 for num in ip.split('.')):
                self.UDP_IP = ip
                self.l_c.setText(f"IP address set to {ip}")
            else:
                raise ValueError("Invalid IP address format")
        except (socket.error, ValueError):
            self.inputID.clear()
            self.l_c.setText("Invalid IP address")
            print(f"Invalid IP address: {ip}")
        # self.UDP_IP = self.inputID.text();


    def create_message(self, direction, speed, mode):
        # MESSAGE : [MODE {R, D} SPEED{0 - 999} DIRECTION {F, B, R, L}]

        # =============MODE================

        if (mode == 1):
            self.MESSAGE = 'R'
            if direction == "Moves Forward" or direction == "Moves Backward":
                direction = direction[6]
            elif direction == "Left Rotation" or direction == "Right Rotation":
                direction = direction[0]
            elif direction == "No movement":
                direction = "S"
        elif (mode == 0):
            self.MESSAGE = 'D'
            if direction != "No movement":
                direction = direction[6]
            else:
                direction = "S"
        # =============MODE================

        # =============SPEED===============
        speed = int(speed)

        if (speed < 10):
            str_speed = f"00{speed}"
        elif (speed < 100):
            str_speed = f"0{speed}"
        else:
            str_speed = speed

        self.MESSAGE += str(str_speed);
        # =============SPEED===============

        # =============DIR=================
        self.MESSAGE += direction
        # =============DIR=================

    def send_message(self, direction, speed, mode):

        self.create_message(direction, speed, mode);

        print("UDP target IP: %s" % self.UDP_IP)
        print("UDP target port: %s" % self.UDP_PORT)
        print("message: %s" % self.MESSAGE)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.UDP_IP != "-":
            sock.sendto(bytes(self.MESSAGE, "utf-8"), (self.UDP_IP, self.UDP_PORT))


