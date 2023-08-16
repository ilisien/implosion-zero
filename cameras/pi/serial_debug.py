from globals import ImageSizePreset, ImageType, FRAME_RES
from image_manipulation import image_from_bytes
from message import Message, MessageData, UnicodeMessageData, ErrorMessageData, RequestImageMessageData, ImageMessageData
from serial_tools import SerialConnection

ser_conn = SerialConnection("COM3",115200)
ser_conn.open_message_queue()
for i in range(5):
    print(ser_conn.message_queue.get())

ser_conn.close_message_thread()