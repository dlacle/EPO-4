import keyboard
import serial
import time

# Transmitting connection takes place over port 5
comport = 'COM7'

# Getting access to the Bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)

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
            fspeed = f"M{speed}\n"
            print(fspeed)  # Register check
            serial_port.write(fspeed.encode())
            previous_speed = speed

        if direction != previous_direction:
           fdirection = f"D{direction}\n"
           print(fdirection)  # Register check
           serial_port.write(fdirection.encode())
           previous_direction = direction

        time.sleep(0.1)  # Adjust sleep time as needed

    # Shutting down the Bluetooth connection with the car
    serial_port.close()

check_keyboard_input()

# # introducing move and angle (the inputs)
# move = ''
# angle = ''
#
#
# while move != 'e':                      # program will ask for movement assigning untill move input 'e'for move
#
#     # assigning the (change in) movement
#     move = input("Move command:")
#     angle = input("Angle command:")
#
#     # forward (w) or backwards (s)
#     if move == 'w':                     # bit faster forward
#         speed += 3
#     elif move == 'ww':                  # maximum speed forward
#         speed = 165
#     elif move == 's':                   # bit faster backward
#         speed -= 3
#     elif move == 'ss':                  # maximum speed backward
#         speed = 135
#     elif move == 'h':                   # hold current speed
#         speed = speed
#     else:                               # any other or no input stops the car
#         speed = 150
#
#     # setting maximum and minimum values of speed
#     if speed >= 165:
#         speed = 165
#     elif speed <= 135:
#         speed = 135
#     else:
#         speed = speed
#
#     fspeed = f"M{speed}\n"              # using f string for speed command
#     print(fspeed)                       # register check
#
#     # direction, left(a) or right(b)
#     if angle == 'a':                    # bit more left
#         direction += 10
#     elif angle == 'aa':                 # maximum (hard) left
#         direction = 200
#     elif angle == 'd':                  # bit more right
#         direction -= 10
#     elif angle == 'dd':                 # maximum (hard) right
#         direction = 100
#     elif angle == 'h':                  # hold current turning direction
#         direction = direction
#     else:                               # any other or no input sets back to strait position (no turning)
#         direction = 150
#
#     # setting maximum and minimum values of direction
#     if direction >= 200:
#         direction = 200
#     elif direction <= 100:
#         direction = 100
#     else:
#         direction = direction
#
#     fdirection = f"D{direction}\n"      # using f string for direction command
#     print(fdirection)                   # register check
#
#     # wait for 1 second before performing movement
#     time.sleep(1)
#
#     # perform the movement
#     serial_port.write(fspeed.encode())
#     serial_port.write(fdirection.encode())
#
#
# # Shut down bluetooth connection with car
# serial_port.close()