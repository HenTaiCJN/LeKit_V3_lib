import dht
import time
from machine import Pin

from pins_const import ports


class dht11:
    def __init__(self, port):
        if port is None:
            print("请指定端口号")

        self.s_pin = Pin(ports[port][1], mode=Pin.IN, pull=Pin.PULL_UP)

        self.dht_sensor = dht.DHT22(self.s_pin)

    def read(self):
        self.dht_sensor.measure()
        temperature = self.dht_sensor.temperature()
        humidity = self.dht_sensor.humidity()
        data = (temperature, humidity)
        time.sleep(0.5)
        return data
