from machine import Pin, ADC

from pins_const import ports


class sound:
    def __init__(self,  port=None):
        if port is None:
            print("请指定端口号")

        self.s_pin = ADC(Pin(ports[port][1], Pin.IN))
        self.s_pin.width(ADC.WIDTH_12BIT)
        self.s_pin.atten(ADC.ATTN_11DB)

    def read(self):
        return self.s_pin.read()
