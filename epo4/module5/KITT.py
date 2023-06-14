import time

import numpy as np
import serial
import serial.tools.list_ports
# from GUI import GUI

def estimate_battery_percentage(current_voltage):
    min_voltage = 17
    max_voltage = 18.6
    voltage_range = max_voltage - min_voltage
    voltage_interval = voltage_range / 10  # Assuming 10 equal intervals

    soc = ((current_voltage - min_voltage) / voltage_interval) * 10
    battery_percentage = max(min(soc, 100), 0)  # Ensure battery percentage is within 0-100 range

    return battery_percentage
class KITT():
    def __init__(self): # called when the class is used to create a new object
        # current_voltage = self.get_status(data = 'voltage')

        # get port info
        ports = serial.tools.list_ports.comports()
        for i in range(len(ports)):
            print(f"{i} - {ports[i].description}")
        comport = 'COM7'
        # comport = ports[int(input(f"Enter device index: \n"))].device

        # global comport
        global serial_port
        # getting access to bluetooth link
        try:
            serial_port = serial.Serial(comport, 115200, rtscts=True)
            print("Port details ->", serial_port)
        except serial.SerialException as var:
            print("Error has occured")
            print("var")
        else:
            print("connected, serial port opened")


    def run_mode(self):
        pass
    def set_beacon(self):
        # Set beacon settings
        # Set bitcode
        self.serial.write(b"C" + (0x3355A780).to_bytes(4, byteorder='big') + b"\n")
        # Set carrier frequency
        self.serial.write(b"F" + (2250).to_bytes(2, byteorder='big') + b"\n")
        # Set bit frequency
        self.serial.write(b"B" + (3000).to_bytes(2, byteorder='big') + b"\n")
        # Set repetition count
        self.serial.write(b"R" + (1250).to_bytes(2, byteorder='big') + b"\n")

        # On
        serial_port.write(b'A1\n')

    def turn(self, direction):
        if direction == 'hard left':
            self.set_angle(200)
        elif direction == 'hard right':
            self.set_angle(100)
        elif direction == 'right':
            self.set_angle(125)
        elif direction == 'left':
            self.set_angle(125)

    def set_dir(self, angle):
        # Limit angle to avoid sending invalid command to KITT
        if 100 <= angle <= 200:
            # Take a given a direction value, convert this to bits and send KITT the command
            self.serial.write(f"D{angle}\n".encode())

    def set_speed(self, speed):
        # Take a given a speed value, convert this to bits and send KITT the command
        if 135 <= speed <= 165:
            # Limit speed to avoid sending invalid command to KITT
            self.serial.write(f"M{speed}\n".encode())

    def get_status(self, data):  # Request status from KITT
        if data == "full":
            # Send S to receive a full status report from KITT
            command = b"S\n"
        elif data == "voltage":
            # Send Sv to receive only the battery voltage
            command = b"Sv\n"
        elif data == "dist":
            # Send Sd to receive only the distance from the ultrasonic sensors
            command = b"Sd\n"
        else:
            # If no valid command is sent, request full status report
            print("Provide valid request, returning full status")
            command = b"S\n"

        self.serial.write(command)
        status = self.serial.read_until(b"\x04")

        if data == "dist":
            # Split the distances up in an array
            distl = int(status.decode().splitlines()[0][3:])
            distr = int(status.decode().splitlines()[1][3:])
            status = np.array([distl, distr])
        elif data == "voltage":
            status = int(status.decode().splitlines()[0][5:-2])
        return status

    def brake(self, speed):
        brake_power = (np.abs(speed) / speed) * 5 + 150
        brake_time = np.abs(speed / 2.3)
        start = time.time()
        T = 0
        while T <= brake_time:
            self.set_speed(brake_power)
            T = T + time.time() - start

    def drive(self, power, turn):
        self.set_angle(turn)
        self.set_speed(power)

    def stop(self):
        # Reset the KITT to its default speed and direction
        self.set_speed(150)
        self.set_dir(150)
    def __del__(self):
        # Disable beacon
        self.serial.write(b"A0\n")
        # Remove object and close serial port
        self.serial.close()

