from machine import Pin

from educore import pin
import neopixel

from pins_const import ports


class RGB:
    def __init__(self, port=None, num=128):
        if port is None:
            print("请指定端口号")

        s_pin = Pin(ports[port][0], Pin.OUT)

        self.num = num
        self.n = neopixel.NeoPixel(s_pin, num)

    def write(self, index, r, g, b):
        for i in index:
            self.n[i] = (r, g, b)
            self.n.write()

    def clear(self):
        for i in range(self.num):
            self.n[i] = (0, 0, 0)
        self.n.write()
