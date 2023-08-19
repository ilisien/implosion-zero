from bin_tools import *

class MessageData: # root message data class
    pass

class UnicodeMessageData(MessageData):
    def __init__(self,message_string):
        self.message_string = message_string
    def __str__(self):
        return f"unicode message '{self.message_string}'"

class ErrorMessageData(MessageData):
    def __init__(self,error_type,error_string):
        self.error_type = error_type
        self.error_string = error_string
    def __str__(self):
        return f"error message '{self.error_string}'"

class RequestImageMessageData(MessageData):
    def __init__(self,camera_id,image_type,image_size_preset):
        self.camera_id = camera_id
        self.image_type = image_type
        self.image_size_preset = image_size_preset
    def __str__(self):
        return f"image request message to camera {self.camera_id} of type {self.image_type} of size {self.image_size_preset}"

class ImageMessageData(MessageData):
    def __init__(self,image_type,image_size_preset,image_bytes):
        self.image_type = image_type
        self.image_size_preset = image_size_preset
        self.image_bytes = image_bytes
    def __str__(self):
        return f"image message of type {self.image_type} of size {self.image_size_preset}"

class Message:
    def __init__(self,type,version,count,data):
        self.type = type
        self.version = version
        self.count = count
        self.data = data
        try:
            self.bin_data, self.data_length = serialize_message_data(type,data)
        except:
            self.bin_data = None
            self.data_length = None
    def __str__(self):
        return f"message object: {self.data}"

def parse_message(bytes):
    header_bytes = bytes[2:12] # first two bytes are for sync
    type = header_bytes[0].decode()
    version = int.from_bytes(header_bytes[1])
    count = int.from_bytes(header_bytes[2:6])
    data_length = int.from_bytes(header_bytes[6:10]) # length after the header

    if version == 0:
        message_bytes = bytes[12:]
        if type == "u": # unicode message
            message_string = message_bytes.decode("utf-8")

            message_data = UnicodeMessageData(message_string)
        elif type == "e": # error message
            error_type = message_bytes[0].decode()
            error_message = message_bytes[1:].decode("utf-8")

            message_data = ErrorMessageData(error_type,error_message)
        elif type == "r": # request image message
            camera_id = int.from_bytes(message_bytes[0])
            image_type = message_bytes[1].decode()
            image_size_preset = message_bytes[2:4].decode()

            message_data = RequestImageMessageData(camera_id,image_type,image_size_preset)
        elif type == "i": # image message
            image_type = message_bytes[0].decode()
            image_size_preset = message_bytes[1:3].decode()
            image_bytes = message_bytes[3:]

            message_data = ImageMessageData(image_type,image_size_preset,image_bytes)
    
    return Message(type,version,count,data_length,message_data)