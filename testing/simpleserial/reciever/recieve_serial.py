import serial

serial_port = 'COM3' # (usb) port to listen on
baud_rate = 115200 # baudrate of serial communication, should be the same as in file uploaded to esp32

try:
    ser = serial.Serial(serial_port,baud_rate) # open serial port connection
    print(f"connected to {ser.name}") # print output with serial name

    while True:
        data = ser.read(2) # read line from serial, decode it, and strip off whitespace
        print(data) # then print that line

except serial.SerialException as e: # if there's a serial error
    print(f"error: {e}") # then print an output that an error has occurred

finally: # and on exit
    ser.close() # close the serial connection
    print("serial connection closed") # output that the serial connection was closed