import serial
# from GUI import *


class KITT:
    def __init__(self, port):  # called when the class is used to create a new object
        self.serial = serial.Serial(port, baudrate=115200, rtscts=True)

    def set_speed(self, speed):
        pass
        # self.serial.write(......)

    def set_angle(self, angle):
        pass
        # self.serial.write(......)

    def stop(self):
        self.set_angle(150)
        self.set_speed(150)

    def __del__(self):
        self.serial.close()


car = KITT('COM7')
print(car.serial)

# print(KITT(3).port)
# KITT()
