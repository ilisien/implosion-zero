import serial, queue, time, threading
from message import Message, MessageData, UnicodeMessageData, ErrorMessageData, RequestImageMessageData, ImageMessageData
from globals import *
from bin_tools import *

def sync_index(byte_segment):
    sync_sequence = bytes([0b00000000,0b11111111])
    try:
        return byte_segment.index(sync_sequence)
    except ValueError:
        return -1


def serial_to_queue(ser,serial_queue,exit_tag):
    while not exit_tag.is_set():
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            serial_queue.put(data)

def decode_header(header):
    sync_seq = header[0:2]
    message_type = header[2:3].decode("utf-8")
    message_version = int.from_bytes(header[3:4])
    message_count = int.from_bytes(header[4:8])
    data_length = int.from_bytes(header[8:12])
    return message_type, message_version, message_count, data_length

def next_message(serial_queue,prev_remainder=None):
    if prev_remainder == None:
        byte_segment = serial_queue.get()
    else:
        byte_segment = prev_remainder

    snc_ind = -1
    while True:
        snc_ind = sync_index(byte_segment)
        if snc_ind == -1:
            byte_segment += serial_queue.get()
        elif len(byte_segment) < snc_ind + 11:
            byte_segment += serial_queue.get()
        else: # we found an byte segment that contains a header, so
            break # break from while loop
    
    head_end_ind = snc_ind + 12

    binary_header = byte_segment[snc_ind:head_end_ind]

    message_type, message_version, message_count, data_length = decode_header(binary_header)

    while True:
        if len(byte_segment[head_end_ind:]) < data_length:
            byte_segment += serial_queue.get()
        else:
            break

    binary_message_data = byte_segment[head_end_ind:head_end_ind+data_length]
    
    message_data = None
    if message_type == MessageType.UNICODE_MESSAGE.value:
        message_data = UnicodeMessageData(binary_message_data.decode("utf-8"))
    elif message_type == MessageType.ERROR_MESSAGE.value:
        pass # todo
    elif message_type == MessageType.REQUEST_IMAGE_MESSAGE.value:
        pass # todo
    elif message_type == MessageType.IMAGE_MESSAGE.value:
        pass # todo, not really necessary on pi side yet though

    new_message = Message(message_type,message_version,message_count,message_data)

    remaining_bytes = byte_segment[head_end_ind+data_length:]

    return new_message, remaining_bytes

def bytes_to_messages(serial_queue,message_queue,exit_tag):
    remainder = None
    while not exit_tag.is_set():
        if not serial_queue.empty():
            message, remainder = next_message(serial_queue,remainder)
            message_queue.put(message)

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
        
        self.serial_queue = None
        self.message_queue = None
    
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

    def open_serial_queue(self):
        self.serial_queue = queue.Queue()
        self.serial_thread_exit_tag = threading.Event()
        self.serial_thread = threading.Thread(target=serial_to_queue,args=(self.ser,self.serial_queue,self.serial_thread_exit_tag,),daemon=True)
        self.serial_thread.start()
    
    def close_serial_queue(self):
        self.serial_thread_exit_tag.set()
    
    def open_message_queue(self):
        if self.serial_queue == None:
            self.open_serial_queue()
        self.message_queue = queue.Queue()
        self.message_thread_exit_tag = threading.Event()
        self.message_thread = threading.Thread(target=bytes_to_messages,args=(self.serial_queue,self.message_queue,self.message_thread_exit_tag,))
        self.message_thread.start()
    
    def close_message_thread(self):
        self.serial_thread_exit_tag.set()
        self.message_thread_exit_tag.set()