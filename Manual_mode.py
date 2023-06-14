import keyboard
import serial
import time
from KITT import KITT

# Transmitting connection takes place over port 5
# comport = 'COM7'

# Getting access to the Bluetooth link
# serial_port = serial.Serial(comport, 115200, rtscts=True)

# Setting initial speed and direction to neutral (150)
speed = 150
direction = 150


def check_keyboard_input():
    global speed, direction

    previous_speed = speed
    previous_direction = direction

    while True:
        if keyboard.is_pressed('w'):
            speed = 165  # Forward speed
        elif keyboard.is_pressed('s'):
            speed = 135  # Backward speed
        else:
            speed = 150  # Default neutral speed

        if keyboard.is_pressed('a'):
            direction = 200  # Left direction
        elif keyboard.is_pressed('d'):
            direction = 100  # Right direction
        else:
            direction = 150  # Default neutral direction

        if keyboard.is_pressed('q'):
            break  # Exit the loop if 'q' is pressed

        # Check if there is a change in speed or direction
        if speed != previous_speed:
            # Sending speed and direction commands to the car
            KITT.set_speed(speed)

            fspeed = f"M{speed}\n"
            print(fspeed)  # Register check

            # serial_port.write(fspeed.encode())
            previous_speed = speed

        if direction != previous_direction:
           KITT.set_speed(direction)
           fdirection = f"D{direction}\n"
           print(fdirection)  # Register check
           # serial_port.write(fdirection.encode())
           previous_direction = direction

        time.sleep(0.1)  # Adjust sleep time as needed

    # Shutting down the Bluetooth connection with the car
    # serial_port.close()

KITT = KITT()
print('port opened')
check_keyboard_input()

KITT.stop()
del KITT