from abc import ABC
from library.messages.Message import Message
from config import LOG_LEVEL, LOG_FORMAT
import logging

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class Observer(ABC):
    def __init__(self):
        self._value = None
        self._observers = []
        self._receiver = None

    @property
    def value(self):
        return self._value

    @value.setter
    def emit(self, value:Message):
        self._value = value
        for callback in self._observers:
            callback(self._value)

    def receive(self):
        return self._receiver()

    def bind_to(self, callback):
        logger.info('Register ' + callback.__name__)
        self._observers.append(callback)

    def bind_receiver_to(self, callback):
        self._receiver = callback