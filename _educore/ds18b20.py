import ds18x20
import onewire
from machine import Pin

from pins_const import ports


class ds18b20:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        s_pin = Pin(ports[port][0], mode=Pin.IN, pull=Pin.PULL_UP)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(s_pin))

    def read(self):  # 创建一个读取温度的函数
        roms = self.ds_sensor.scan()  # 扫描总线上的设备
        self.ds_sensor.convert_temp()  # 温度转换
        for rom in roms:  # 循环打印出设备列表
            temp = self.ds_sensor.read_temp(rom)  # 读出该设备的温度
            if isinstance(temp, float):  # 以小数点后2位输出，例如23.35
                temp = round(temp, 2)
                return temp
        return 0
