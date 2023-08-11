import serial
from message import Message, MessageData, UnicodeMessageData, ErrorMessageData, RequestImageMessageData, ImageMessageData
from globals import *
from bin_tools import *

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
    
    def send_message(self,message,update_count=True):
        if self.ser == None:
            print("serial not connected!")
            return
        
        if update_count:
            self.messages_sent += 1
            message.count = self.messages_sent
        message_packet = serialize_message(message)

        try:
            self.ser.write(message_packet)
            print(f"successfully sent '{message}'")
            return message_packet, message
        except:
            print(f"unable to send '{message}'")
            return message_packet, message

    def read_message(self):
        search_byte = None
        while search_byte != 0b00000000:
            search_byte = self.ser.read(1)