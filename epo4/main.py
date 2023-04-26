# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


serial.Serial(port, baudrate) # This command is used to initialize a serial connection. Theport argument specifies the serial port to use (e.g. "COM1" on Windows or "/dev/rfcomm0" onLinux), and the baud-rate argument specifies the data rate in bits per second.
serial.write(data) # This command is used to send data over the serial connection. The data argument is a bytes object that contains the data to be sent.
serial.readline() # This command is used to read a line of data from the serial connection. Itblocks until a line of data is received.
serial.read(size) #This command is used to read a specified number of bytes from the serial connection. It blocks until the specified number of bytes is received.
serial.flush() # This command is used to flush the input and output buffers of the serial con-nection
serial.close() # This command is used to close the serial connection

#https://pyserial.readthedocs.io/en/latest/pyserial.html
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
