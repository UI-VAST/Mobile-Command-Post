import serial

port = "/dev/serial0"
baud = 19200

ir = serial.Serial(port, baudrate=baud, timeout=5)
ir.reset_input_buffer()
ir.flush()

inp = input()
while inp != 'exit':
    ir.write(inp)
    inp = input()
