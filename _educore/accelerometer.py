import time

from machine import Pin, I2C, SoftI2C

from adxl import adxl345
from pins_const import ports


class accelerometer:
    def __init__(self, port):
        if port is None:
            print("请指定端口号")

        sda = Pin(ports[port][1])
        scl = Pin(ports[port][0])
        i2c = SoftI2C(sda=sda, scl=scl, freq=10000)

        self.snsr = adxl345(i2c)

    @property
    def X(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return x

    @property
    def Y(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return y

    @property
    def Z(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return z

    def shake(self):
        if self.snsr is not None:
            x1, y1, z1 = self.snsr.readXYZ()
            time.sleep(0.5)
            x2, y2, z2 = self.snsr.readXYZ()
            time.sleep(0.5)
            if abs(x1 - x2) > 20 or abs(y1 - y2) > 20 or abs(z1 - z2) > 20:
                return True
            else:
                return False
