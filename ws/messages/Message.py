from datetime import datetime

class Message:
    def __init__(self, type, sender, payload):
        self.__type = type
        self.__sender = sender
        self.__timestamp = str(datetime.now())
        self.__payload = payload

    def get_type(self):
        return self.__type

    def get_sender(self):
        return self.__sender

    def get_timestamp(self):
        return self.__timestamp

    def get_payload(self):
        return self.__payload

