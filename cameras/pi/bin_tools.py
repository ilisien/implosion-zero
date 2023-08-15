from globals import *

def int2bin(integer,nbytes=1):
    return integer.to_bytes(nbytes)

def str2bin(string):
    return string.encode('utf-8')

def serialize_message_data(message_type,data):
    if message_type == MessageType.UNICODE_MESSAGE.value:
        bin_data = [*str2bin(data.message_string)]
    elif message_type == MessageType.ERROR_MESSAGE.value:
        bin_data = [*str2bin(data.error_type),
                    *str2bin(data.error_string)]
    elif message_type == MessageType.REQUEST_IMAGE_MESSAGE.value:
        bin_data = [*int2bin(data.camera_id),
                    *str2bin(data.image_type),
                    *str2bin(data.image_size_preset)]
    elif message_type == MessageType.IMAGE_MESSAGE.value:
        pass # todo, not really necessary on pi side yet though

    bin_data_length = len(bin_data)
    return bin_data, bin_data_length

def serialize_message(message):
    message_packet = bytes([0b00000000, 0b11111111])
    header = [*str2bin(message.type),
              *int2bin(message.version),
              *int2bin(message.count,4),
              *int2bin(message.data_length,4)]
    message_packet += bytes(header)
    
    message_packet += bytes(message.bin_data)
    return message_packet