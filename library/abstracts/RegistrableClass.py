from abc import ABC
from library.observers.Observer import Observer

class RegistrableClass(ABC):
    def __init__(self):
        self.observers = []
        self.receiver = None
        super().__init__()

    def register_observer(self, observers:Observer, callback):
        self.observers.append(observers)
        self.observers[len(self.observers)-1].bind_to(callback)

    def register_receiver(self, observer:Observer, callback):
        self.receiver = observer
        self.receiver.bind_receiver_to(callback)