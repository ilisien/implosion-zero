class Message():
    def __init__(self,bytes):
        header_bytes = bytes[2:12]
        message_bytes = bytes[12:]
        self.type = header_bytes[0].decode()
        self.version = int.from_bytes(header_bytes[1])
        self.count = int.from_bytes(header_bytes[2:6])
        self.data_length = int.from_bytes(header_bytes[6:10])
        