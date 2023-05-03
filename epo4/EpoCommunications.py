import serial

def EpoCommunications(code,connection):
    # connect to bluetooth KITT
    #set transmitting connection
    comport = 'COM5'

    # set baudrate
    baudrate = 115200
    while Connection == true:
    serial_port = serial.Serial(comport, baudrate, rtscts=True)

    # send command to KITT
    serial_port.write(b'code\n')

        #example motor/direction control
            # serial_port.write(b'D169\n')
            # serial_port.write(b'M135\n')

        # Audio beacon command
            #serial_port.write(b'A1\n')  --on
            # serial_port.write(b'A0\n') --off


            # carrier_frequency = 10000.
            # to_bytes(2, byteorder='big')
            # serial_port.write(b'F' + carrier_frequency + b'\n')

            # bit_frequency = 5000.
            # to_bytes(2, byteorder='big')
            # serial_port.write(b'B' + bit_frequency + b'\n')

            # repetition_count = 2500.
            # to_bytes(2, byteorder='big')
            # serial_port.write(b'R' + repetition_count + b'\n')

            # code = 0xDEADBEEF.to_bytes(4, byteorder='big')
            # serial_port.write(b'C' + code + b'\n')

    # Status command from KITT
        # serial_port.write(b'S\n')
        # status = serial_port.read_until(b'\x04')

    # close connection
    serial_port.close()

    return(status, )

