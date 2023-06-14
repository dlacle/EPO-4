import serial
from GUI import GUI

def estimate_battery_percentage(current_voltage):
    min_voltage = 16 #?????
    max_voltage = 18.6
    voltage_range = max_voltage - min_voltage
    voltage_interval = voltage_range / 10  # Assuming 10 equal intervals

    soc = ((current_voltage - min_voltage) / voltage_interval) * 10
    battery_percentage = max(min(soc, 100), 0)  # Ensure battery percentage is within 0-100 range

    return battery_percentage
class KITT():
    def __init__(self): # called when the class is used to create a new object
        # current_voltage = self.get_status(data = 'voltage')
        # port = GUI(estimate_battery_percentage(current_voltage))
        port = "COM7"
        self.serial = serial.Serial(port,baudrate=115200,rtscts=True)
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

    def stop(self):
        # Reset the KITT to its default speed and direction
        self.set_speed(150)
        self.set_dir(150)
    def __del__(self):
        # Disable beacon
        self.serial.write(b"A0\n")
        # Remove object and close serial port
        self.serial.close()



KITT()