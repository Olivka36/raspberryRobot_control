#include <WiFi.h>
#include <WiFiUdp.h>

#include <Wire.h>
#include <iarduino_I2C_Motor.h>                 //  Библиотека для управления моторами

iarduino_I2C_Motor mot_RB(0x09);                //  Правый задний мотор
iarduino_I2C_Motor mot_LB(0x0A);                //  Левый задний мотор
iarduino_I2C_Motor mot_RF(0x0C);                //  Правый передний мотор
iarduino_I2C_Motor mot_LF(0x0B);                //  Левый передний мотор

const char *ssid = "DESKTOP-SFJ17IN 7960";
const char *password = "#Y9q1728";
const int UDP_PORT = 5005;

WiFiUDP udp;
char packetBuffer[255];
char writeBuffer[255];

void setup() {
  //============SETUP WHEELS============
  delay(500);                                   // * Ждём завершение переходных процессов связанных с подачей питания.

  mot_LB.begin();                               //  Инициализация работы моторов
  mot_LF.begin();
  mot_RB.begin();
  mot_RF.begin();
  
  mot_LB.setDirection(false);                   //  Задаём направление вращения для левого  мотора: против часовой стрелки при положительных скоростях и по при отрицательных.
  mot_LF.setDirection(false);
  mot_RF.setDirection(true);                    //   Задаём направление вращения для правого мотора: по часовой стрелке при положительных скоростях и против при отрицательных.
  mot_RB.setDirection(true);

  mot_LB.radius = 60;                           //   Указываем радиус левого  колеса в мм (значение используется для движения на заданное растояние).
  mot_LF.radius = 60;                           //   Указываем радиус правого колеса в мм (значение используется для движения на заданное растояние).
  mot_RB.radius = 60;
  mot_RF.radius = 60;
  //============SETUP WHEELS============
  
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  
  //============CHECK WIFI CONNECTION============
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.SSID());

  Serial.print("Assigned IP Address: ");
  Serial.println(WiFi.localIP());
  //============CHECK WIFI CONNECTION============


  //UDP begin
  if(WiFi.status() == WL_CONNECTED)
  {
    udp.begin(UDP_PORT);
    Serial.print("Listening UDP port ");
    Serial.println(UDP_PORT);    
  }
}


void move_forward(int speed)
{
  Serial.println("Moving forward");
  // Движение вперёд:                           
  mot_LF.setSpeed( speed, MOT_RPM); 
  mot_RF.setSpeed( speed, MOT_RPM);
  mot_LB.setSpeed( speed, MOT_RPM);
  mot_RB.setSpeed( speed, MOT_RPM);
}


void move_backward(int speed)
{
  Serial.println("Moving backward");
  // Движение назад:                            
  mot_LF.setSpeed( -speed, MOT_RPM);
  mot_RF.setSpeed( -speed, MOT_RPM);
  mot_LB.setSpeed( -speed, MOT_RPM);
  mot_RB.setSpeed( -speed, MOT_RPM);
}

void rotate_left(int speed)
{
  Serial.println("Rotating left");
  // Движение влево:                            
  mot_LF.setSpeed( -speed, MOT_RPM);
  mot_RF.setSpeed( speed, MOT_RPM);
  mot_LB.setSpeed( -speed, MOT_RPM);
  mot_RB.setSpeed( speed, MOT_RPM);
}

void move_left(int speed)
{
  Serial.println("Moving left");
  // Движение влево:                            
  mot_LF.setSpeed( -speed, MOT_RPM);
  mot_RF.setSpeed( speed, MOT_RPM);
  mot_LB.setSpeed( speed, MOT_RPM);
  mot_RB.setSpeed( -speed, MOT_RPM);
}

void rotate_right(int speed)
{
  Serial.println("Rotating right");
  // Движение вправо:                          
  mot_LF.setSpeed( speed, MOT_RPM);
  mot_RF.setSpeed( -speed, MOT_RPM);
  mot_LB.setSpeed( speed, MOT_RPM);
  mot_RB.setSpeed( -speed, MOT_RPM);
}

void move_right(int speed)
{
  Serial.println("Moving right");
  // Движение вправо:                          
  mot_LF.setSpeed( speed, MOT_RPM);
  mot_RF.setSpeed( -speed, MOT_RPM);
  mot_LB.setSpeed( -speed, MOT_RPM);
  mot_RB.setSpeed( speed, MOT_RPM);
}


int get_speed()
{
  
  return ((int)packetBuffer[1] - 48) * 100 + ((int)packetBuffer[2] - 48) * 10 + ((int)packetBuffer[3] - 48);
}

void stop()
{
  Serial.println("Stopping");
  // Остановка:                                 
  mot_LF.setSpeed( 0, MOT_RPM);                   
  mot_RF.setSpeed( 0, MOT_RPM);
  mot_LB.setSpeed( 0, MOT_RPM);
  mot_RB.setSpeed( 0, MOT_RPM);
}

void rotation_mode()
{
  int speed = get_speed();

  if (packetBuffer[4] == 'F')
  {
    move_forward(speed);
  }
  else if(packetBuffer[4] == 'B')
  {
    move_backward(speed);
  }
  else if(packetBuffer[4] == 'R')
  {
    rotate_right(speed);
  }
  else if(packetBuffer[4] == 'L')
  {
    rotate_left(speed);
  }
  else if(packetBuffer[4] == 'S')
  {
    stop();
  }
  else
  {
    Serial.println("Uknownt command!");
  }
}

void drive_mode()
{
  int speed = get_speed();

  if (packetBuffer[4] == 'F')
  {
    move_forward(speed);
  }
  else if(packetBuffer[4] == 'B')
  {
    move_backward(speed);
  }
  else if(packetBuffer[4] == 'R')
  {
    move_right(speed);
  }
  else if(packetBuffer[4] == 'L')
  {
    move_left(speed);
  }
  else if(packetBuffer[4] == 'S')
  {
    stop();
  }
  else
  {
    Serial.println("Uknownt command!");
  }
}


void loop() 
{
  //============RECIEVING MESSAGE============
  if (WiFi.status() == WL_CONNECTED)
  {
    int packetSize = udp.parsePacket();

    if (packetSize)
    {
      udp.read(packetBuffer, packetSize);

      if(packetBuffer[0] == 'D')
        drive_mode();
      else if (packetBuffer[0] == 'R')
        rotation_mode();
      
    }

    udp.beginPacket("192.168.137.1", 5005);
    sprintf(writeBuffer, "%.3f;%.3f;%.3f;%.3f;", mot_LF.getSpeed(MOT_RPM),
            mot_RF.getSpeed(MOT_RPM), mot_LB.getSpeed(MOT_RPM), mot_RB.getSpeed(MOT_RPM));
    Serial.println(writeBuffer);
    udp.write(writeBuffer, 255);
    bool flag = udp.endPacket();
    if(flag)
     Serial.println("Success");
      
  }
  //============RECIEVING MESSAGE============
}