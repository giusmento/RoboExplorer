from abc import ABC

class RegistrableClass(ABC):
    def __init__(self):
        self.observers = []
        super().__init__()

    def register_observer(self, observers, callback):
        self.observers.append(observers)
        self.observers[len(self.observers)-1].bind_to(callback)