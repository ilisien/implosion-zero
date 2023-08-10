import serial
from message import Message, MessageData, UnicodeMessageData, ErrorMessageData, RequestImageMessageData, ImageMessageData
from globals import *

def chr2bin(character,nbytes=1):
    return format(ord(character),f"0{nbytes*8}b")

def int2bin(integer,nbytes=1):
    return format(integer,f"0{nbytes*8}b")

def str2bin(string):
    return string.encode('utf-8')

class SerialConnection:
    def __init__(self,port,baud_rate,should_connect = True):
        self.port = port
        self.baud_rate = baud_rate
        self.messages_sent = 0
        self.messages_recieved = 0
        if should_connect:
            self.ser = serial.Serial(port,baud_rate)
        else:
            self.ser = None
    
    def connect(self):
        if self.ser == None:
            self.ser == serial.Serial(self.port,self.baud_rate)
        else:
            print(f"port {self.port} already connected!")

    def disconnect(self):
        if self.ser != None:
            self.ser.close()
        else:
            print(f"port {self.port} already disconnected!")
    
    def send_message(self,message):
        if self.ser == None:
            print("serial not connected!")
            return

        message_packet = bytearray().extend([0b00000000, 0b11111111])
        header = [chr2bin(message.type),
                  int2bin(message.version),
                  int2bin(message.messages_sent + 1,4),
                  int2bin(message.data_length,4)]
        message_packet.extend(header)
        

        if message.type == MessageType.UNICODE_MESSAGE:
            message_packet.extend(str2bin(message.data.message_string))
        elif message.type == MessageType.ERROR_MESSAGE:
            message_packet.extend([chr2bin(message.data.error_type),
                                   str2bin(message.data.error_string)])
        elif message.type == MessageType.REQUEST_IMAGE_MESSAGE:
            message_packet.extend([int2bin(message.data.camera_id),
                                   chr2bin(message.data.image_type),
                                   chr2bin(message.data.image_size_preset,2)])
        elif message.type == MessageType.IMAGE_MESSAGE:
            pass
        
        try:
            self.ser.write(message_packet)
            print(f"successfully sent '{message}'")
            self.messages_sent += 1
            return message_packet, message
        except:
            print(f"unable to send '{message}'")
            return message_packet, message

    def read_message(self):
        search_byte = None
        while search_byte != 0b00000000:
            search_byte = self.ser.read(1)