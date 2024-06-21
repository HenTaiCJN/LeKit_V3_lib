from machine import Pin

from educore import pin
from pins_const import ports


class TSD:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        self.s_pin = Pin(ports[port][0], Pin.IN)

    def read(self):
        return self.s_pin.value()
