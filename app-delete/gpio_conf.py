import gpiozero
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero.pins.pigpio import PiGPIOFactory

def gpio_conf(MOCK_GPIO, PIGPIO_ADDR):
    if MOCK_GPIO:
        if PIGPIO_ADDR is not None:
            factory = PiGPIOFactory(host=PIGPIO_ADDR)
        else:
            factory = MockFactory(pin_class=MockPWMPin)
        gpiozero.Device.pin_factory = factory