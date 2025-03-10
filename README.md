![Socket](https://img.shields.io/badge/Socket-4F75C3?style=for-the-badge&logo=python&logoColor=white) ![PyQt](https://img.shields.io/badge/PyQt-41CD52?style=for-the-badge&logo=qt&logoColor=white) 

### Controlling a Raspberry Pi Robot with a GUI 🏎
### Управление роботом на Raspberry Pi Pico с помощью графического интерфейса

Для тестирования программного модуля использовался физический робот, на котором установлены колеса Илона, плата Raspberry Pi Pico и моторы-редукторы FLASH-I2C.

### 🕹 Особенности работы:
Робот управляется с помощью двумерного джойстика в графическом интерфейсе. Доступны 2 режима управления:  
1. Робот двигается влево-вправо в своем первоначальном положении.
2. Робот разворачивается на месте (вращается вокруг своей оси). <br>

Выбор режима управления осуществляется с помощью переключателя рядом с джойстиком. В верхнем правом углу экрана расположено поле для ввода IP-адреса робота. По кнопке ***connect*** происходит подключение к физическому роботу. Ниже отображается информация о том, удалось ли подключиться. Далее идет два поля: слева показывается формируемая управления, справа - фактическая скорость колес робота (при успешном подключении).

<img src="https://github.com/Olivka36/raspberryRobot_control/blob/main/gui.png" width="500"/>
 
### 🗂 Структура программного модуля:
* ***Robot***: класс, отвечающий за отображение робота на поле для симуляции его движения (область слева).
* ***Connection***: класс для отправки команды роботу и получения данных с него.
* ***Joystick***: класс, который рисует двумерный джойстик и обрабатывает его движения для формирования команд роботу.
* ***ToSwitch***: класс, отвечающий за переключение между режимами управления
* ***raspberry_pgm.ino***: код, загруженный на Raspberry Pi для управления моторами.  

Для отправки сообщений роботу используется механизм pyqtSignal: при изменении состояния джойстика эмитируется сигнал, который подключен к слоту для отправки сообщений.  

### ❌ Недочеты:
В системе отсутствует проверка IP-адреса на валидность. Реализована лишь базовая проверка: проверяется количество точек, цифры и их значения (не более 256).
