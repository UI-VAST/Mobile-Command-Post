import serial

port = "/dev/serial0"
baud = 19200

ir = serial.Serial(port, baudrate=baud, timeout=5)
ir.reset_input_buffer()
ir.flush()

inp = input()
while inp != 'exit':
    ir.write(bytes(inp, "utf-8"))
    while 1:
        if ir.in_waiting:
            while ir.in_waiting:
                temp = ir.readline()
                print(temp)
                print(temp.decode())
            break
    inp = input()
