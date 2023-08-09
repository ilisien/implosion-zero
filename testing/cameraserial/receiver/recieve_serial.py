import serial
from PIL import Image
from IPython.display import display
import subprocess

serial_port = 'COM3' # (usb) port to listen on
baud_rate = 115200 # baudrate of serial communication, should be the same as in file uploaded to esp32

try:
    ser = serial.Serial(serial_port,baud_rate) # open serial port connection
    print(f"connected to {ser.name}") # print output with serial name

    while True:
        image = Image.new("RGB", (96, 96))
        rgb_tuples = []
        image_bytes = ser.read(18432) # read line from serial, decode it, and strip off whitespace
        #print([bin(byte) for byte in data]) # then print that line
        for i in range(0, len(image_bytes), 2):
            rgb565 = (image_bytes[i] << 8) | image_bytes[i + 1]
            r = (rgb565 >> 11) & 0x1F
            g = (rgb565 >> 5) & 0x3F
            b = rgb565 & 0x1F
            r = (r << 3) | (r >> 2)
            g = (g << 2) | (g >> 4)
            b = (b << 3) | (b >> 2)
            rgb_tuples.append((r, g, b))

        # Put the RGB tuples into the image
        image.putdata(rgb_tuples)

        temp_image_path = "/Users/ilisi/Desktop/implosion-zero/testing/cameraserial/receiver/temp_image.png"
        image.save(temp_image_path)

        # Open the image using the 'code' command in the integrated terminal
        subprocess.run(["code", temp_image_path], check=True)
        print(len(image_bytes))


except serial.SerialException as e: # if there's a serial error
    print(f"error: {e}") # then print an output that an error has occurred

finally: # and on exit
    ser.close() # close the serial connection
    print("serial connection closed") # output that the serial connection was closed