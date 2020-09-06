from abc import ABC, abstractmethod
from library.messages.Message import Message

class Observer(ABC):
    def __init__(self, message:Message):
        self._value = message
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def emit(self, value:Message):
        self._distance = value
        for callback in self._observers:
            callback(self._distance)

    def bind_to(self, callback):
        print('Register ' + callback.__name__)
        self._observers.append(callback)