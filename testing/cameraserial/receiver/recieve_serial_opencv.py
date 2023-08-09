import serial, numpy as np, cv2
from PIL import Image
from IPython.display import display


serial_port = 'COM3' # (usb) port to listen on
baud_rate = 115200 # baudrate of serial communication, should be the same as in file uploaded to esp32

def rgb565_to_rgb(byte1, byte2):
    r = ((byte1 & 0xF8) >> 3) << 3
    g = (((byte1 & 0x07) << 3) | ((byte2 & 0xE0) >> 5)) << 2
    b = (byte2 & 0x1F) << 3
    return r, g, b

def bytes_to_image(byte_list, width, height):
    image_data = np.zeros((height, width, 3), dtype=np.uint8)
    byte_index = 0

    for y in range(height):
        for x in range(width):
            byte1 = byte_list[byte_index]
            byte2 = byte_list[byte_index + 1]
            r, g, b = rgb565_to_rgb(byte1, byte2)
            image_data[y, x] = [b, g, r]  # OpenCV uses BGR format

            byte_index += 2

    return image_data

try:
    ser = serial.Serial(serial_port,baud_rate) # open serial port connection
    print(f"connected to {ser.name}") # print output with serial name

    while True:
        #image = Image.new("RGB", (800, 600))
        #rgb_tuples = []
        image_bytes = ser.read(236800) # read line from serial, decode it, and strip off whitespace
        #print([bin(byte) for byte in data]) # then print that line
        image = bytes_to_image(image_bytes, 400, 296)

        # Display the image using OpenCV
        cv2.imshow('Converted Image', image)
        cv2.waitKey(1)
        #cv2.destroyAllWindows()

        print(len(image_bytes))


except serial.SerialException as e: # if there's a serial error
    print(f"error: {e}") # then print an output that an error has occurred

finally: # and on exit
    ser.close() # close the serial connection
    print("serial connection closed") # output that the serial connection was closed