import json
import time

from machine import UART

from pins_const import ports


class ps2but(object):

    def __init__(self, port=None):
        self.data = {'X': 761, 'Y': 767, 'Button': 0}
        if port is None:
            print("请指定端口号")

        tx = ports[port][0]
        rx = ports[port][1]

        self.uart = UART(1, baudrate=9600, rx=rx, tx=tx)

    def read(self):
        msg = ""
        self.data = {'X': 761, 'Y': 767, 'Button': 0}
        try:
            self.uart.write(b'readdown')
            time.sleep(1 / 10)
            if self.uart.any():
                msg = self.uart.readline().decode()
            if msg == "":
                return
            self.data = json.loads(msg)
        except Exception as e:
            pass

    def getX(self):
        self.read()
        return self.data['X']

    def getY(self):
        self.read()
        return self.data['Y']

    def getBt(self):
        self.read()
        return 0 if self.data['Button'] else 1
