from globals import ImageSizePreset, ImageType, FRAME_RES
from image_manipulation import image_from_bytes
from message import Message, MessageData, UnicodeMessageData, ErrorMessageData, RequestImageMessageData, ImageMessageData
from serial_tools import SerialConnection
import serial, numpy as np, cv2
from bin_tools import serialize_message

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

ser_conn = SerialConnection("COM3",115200)
ser_conn.open_message_queue()

request_image_message = Message("r",0,0,RequestImageMessageData(0,"c","CI"))

for i in range(100):
    ser_conn.send_message(request_image_message)
    recieved_message = ser_conn.message_queue.get()
    print(f"recieved message: {recieved_message}")
    image_size = FRAME_RES[recieved_message.data.image_size_preset]
    image_data = bytes_to_image(recieved_message.data.image_bytes,image_size[0],image_size[1])
    cv2.imshow('Image', image_data)
    cv2.waitKey(1)

cv2.destroyAllWindows()
ser_conn.close_message_thread()