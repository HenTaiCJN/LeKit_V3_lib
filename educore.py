import gc
from machine import Pin, ADC, unique_id
import time

from pins_const import ports

chip_id = unique_id()
uuid = ':'.join(['{:02x}'.format(byte) for byte in chip_id])


# oled
class _oled:

    def __init__(self):
        from ssd1306cn import oled1306
        self.oled = oled1306()

    def print(self, txt):
        self.oled.displayclear()
        self.oled.displaytxtauto(txt, 0, 0)
        self.oled.displayshow()
        gc.collect()

    def clear(self):
        self.oled.displayclear()
        self.oled.displayshow()


oled = _oled()


class speaker:
    def __init__(self, port):
        from _educore.speaker import speaker as sp
        self.s = sp(port=port)

    def tone(self, freq, dual=None, durl=None):
        if dual is None:
            dual = durl
        self.s.tone(freq=freq, durl=dual)

    def stop(self):
        self.s.stop()


# 电机控制
class parrot:
    M1 = 1
    M2 = 2

    def __init__(self, port):
        from _educore.parrot import parrot as pr
        self.p = pr(port=port)

    def speed(self, speed=None):
        self.p.set_speed(speed)
        gc.collect()


# 舵机控制
class servo:
    def __init__(self, port):
        from _educore.servo import servo as sv
        time.sleep(1)
        self.s = sv(port=port)

    def angle(self, value=None, radians=None):
        self.s.angle(value, radians)


# RGB
class rgb:
    def __init__(self, port=None, num=128):
        from _educore.rgb import RGB
        self.rgb = RGB(port=port, num=num)
        gc.collect()

    def write(self, index, r, g, b):
        self.rgb.write(index, r, g, b)
        gc.collect()

    def clear(self):
        self.rgb.clear()
        gc.collect()


# 读取声音
class sound:

    def __init__(self, port=None):
        from _educore.sound import sound as sd
        self.s = sd(port=port)

    def read(self):
        return self.s.read()


# 读取光线
class light:
    def __init__(self, port=None):
        from _educore.light import light as lg
        self.s = lg(port=port)

    def read(self):
        return self.s.read()


# 板载按键
class button:
    a = '33'
    b = '14'

    def __init__(self, ch=None):
        from _educore.button import button as btn
        self.btn = btn(ch=ch)

    def status(self):
        return self.btn.status()

    @property
    def event_pressed(self):
        return self.btn.event_pressed

    @event_pressed.setter
    def event_pressed(self, callback):
        self.btn.event_pressed = callback


# 加速度传感器
class accelerometer:

    def __init__(self, port=None):
        from _educore.accelerometer import accelerometer as acc
        self.acc = acc(port=port)

    def X(self):
        gc.collect()
        return self.acc.X

    def Y(self):
        gc.collect()
        return self.acc.Y

    def Z(self):
        gc.collect()
        return self.acc.Z

    def shake(self):
        gc.collect()
        return self.acc.shake()


# dht11温湿度
class dht:

    def __init__(self, port=None):
        from _educore.dht11 import dht11 as dt
        self.dht = dt(port=port)

    def read(self):
        return self.dht.read()


# DS18b20温度传感器
class ds18b20:

    def __init__(self, port=None):
        from _educore.ds18b20 import ds18b20 as ds
        self.ds = ds(port=port)

    def read(self):
        return self.ds.read()


# 超声波测距
class ultrasonic:

    def __init__(self, port=None):
        from _educore.ultrasonic import Ultrasonic
        self.u = Ultrasonic(port=port)

    def distance(self):
        return self.u.distance()

    def distance_mm(self):
        return self.u.distance_mm()


class rfid:
    def __init__(self, port=None, address=None):
        from _educore.rfid import Scan_Rfid
        self.rfid = Scan_Rfid(port=port, address=address)

    def scanning(self, wait=True):
        return self.rfid.scanning(wait=wait)


class tsd:

    def __init__(self, port=None):
        from _educore.tsd import TSD
        self.tsd = TSD(port=port)

    def read(self):
        return self.tsd.read()


class pressure:

    def __init__(self, port=None):
        from _educore.pressure import pressure as ps
        self.ps = ps(port=port)

    def read(self):
        gc.collect()
        return self.ps.read()


class compass:

    def __init__(self, port=None):
        from _educore.compass import qmc5883 as qmc
        self.qmc = qmc(port=port)

    def adjust(self):
        self.qmc.adjust()
        gc.collect()

    def direction(self):
        gc.collect()
        return self.qmc.direction()

    def getx(self):
        return self.qmc.getx()

    def gety(self):
        return self.qmc.gety()

    def getz(self):
        return self.qmc.getz()


# 蓝牙HID设备模块
class Keyboard:
    CLICK = 1
    DCLICK = 2
    SPACE = 0x2C
    ENTER = 0x28
    CTRL = 0xE0
    SHIFT = 0xE1
    ALT = 0xE2
    LEFT = 0x50
    RIGHT = 0x4F
    DOWN = 0x51
    UP = 0x52
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '0'

    def __getattr__(self, letter):
        return letter


keycode = Keyboard()


class hid:
    def __init__(self, name):
        from _educore.hid import HID
        self.ble = HID(name)
        gc.collect()

    def isconnected(self):
        return self.ble.isconnected()

    def keyboard_send(self, code):
        self.ble.keyboard_send(code)
        gc.collect()

    def mouse_key(self, code):
        self.ble.mouse_key(code)
        gc.collect()

    def mouse_move(self, x, y, wheel=0):
        self.ble.mouse_move(x=x, y=y, wheel=wheel)


# 连接wifi

class wifi:
    import wificonnect as wc
    def __init__(self):
        pass

    @classmethod
    def connect(cls, ssid, psd, timeout=10000):
        cls.wc.start()
        cls.wc.connect(ssid, psd, timeout)
        gc.collect()

    @classmethod
    def close(cls):
        cls.wc.close()
        gc.collect()

    @classmethod
    def status(cls):
        cls.wc.status()

    @classmethod
    def info(cls):
        cls.wc.info()


# MQTT
class mqttclient:
    from _educore.mqtt import MQTTClient
    def __init__(self):
        pass

    @classmethod
    def connect(cls, server, port, client_id='', user='', psd=''):
        cls.MQTTClient.connect(server=server, port=port, client_id=client_id, user=user, psd=psd)

    @classmethod
    def connected(cls):
        return cls.MQTTClient.connected()

    @classmethod
    def publish(cls, topic, content):
        cls.MQTTClient.publish(topic=topic, content=content)

    @classmethod
    def message(cls, topic):
        return cls.MQTTClient.receive(topic=topic)

    @classmethod
    def received(cls, topic, callback):
        cls.MQTTClient.Received(topic=topic, callback=callback)


class webcamera:
    from _educore.webcamera import webcamera

    @classmethod
    def connect(cls, id):
        cls.webcamera.connect(id)

    @classmethod
    def result(cls):
        return cls.webcamera.result()


def get_dict_from_file(filename):
    # 打开文件并读取所有行
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 初始化空字典
    dic = {}

    # 遍历每一行并生成键值对
    for line in lines:
        # 去除行末尾的换行符
        line = line.rstrip('\n')

        # 将行内容拆分为键和值
        key, value = line.split(' ', 1)

        # 如果键已经存在于字典中，则忽略该行
        if key in dic:
            continue

        # 将键值对添加到字典中
        dic[key] = value

    # 返回生成的字典
    gc.collect()
    return dic


def get_dict_from_str(s):
    result_dict = {}

    # 使用分号或换行符分割字符串
    entries = s.replace('\n', ';').split(';')

    for entry in entries:
        # 移除可能存在的多余空格
        entry = entry.strip()

        # 使用空格分割键值对
        key_value = entry.split(None, 1)

        # 确保有两个元素，否则跳过当前条目
        if len(key_value) == 2:
            key, value = key_value
            result_dict[key] = value

    gc.collect()
    return result_dict


class led:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        self.led_pin = Pin(ports[port][0], Pin.OUT, pull=-1)
        self.led_pin.value(0)

    def on(self):
        self.led_pin.value(1)

    def off(self):
        self.led_pin.value(0)


class singlebutton:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")
        self.s_pin = Pin(ports[port][0], Pin.IN, pull=-1)

    def read(self):
        return self.s_pin.value()


class fourfoldbut:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        self.s_pin = Pin(ports[port][1], Pin.IN, pull=-1)

        self.adc_sig = ADC(self.s_pin)
        self.adc_sig.width(ADC.WIDTH_12BIT)
        self.adc_sig.atten(ADC.ATTN_11DB)

    def read(self):
        gc.collect()
        return self.adc_sig.read()

    def button(self):
        if self.read() == 0:
            return 'A'
        elif 800 < self.read() < 1500:
            return 'B'
        elif 1800 < self.read() < 2500:
            return 'C'
        elif 3000 < self.read() < 4095:
            return 'D'
        else:
            return None


class IR:

    def __init__(self, port=None):
        from _educore.ir import IR as irremote
        self.irr = irremote(port=port)

    def setcb(self, func):
        self.irr.setcb(func)

    def read(self):
        return self.irr.read()


class apds:
    def __init__(self, port=None):
        from _educore.apds import apds as apdsremote
        self.apds = apdsremote(port)

    def read(self):
        return self.apds.read()

    def readProximity(self):
        return self.apds.readProximity()

    def readLight(self):
        return self.apds.readLight()


class linefinder:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        self.s1_pin = Pin(ports[port][1], mode=Pin.IN, pull=-1)
        self.s2_pin = Pin(ports[port][0], mode=Pin.IN, pull=-1)

    def reads1(self):
        return self.s1_pin.value()

    def reads2(self):
        return self.s2_pin.value()


class ps2but(object):

    def __init__(self, port=None):
        from _educore.ps2btn import ps2but
        self.btn = ps2but(port)

    def getX(self):
        return self.btn.getX()

    def getY(self):
        return self.btn.getY()

    def getBt(self):
        return self.btn.getBt()


class dig_display:
    def __init__(self, port=None):
        from tm1637 import TM1637

        dio = Pin(ports[port][0])
        clk = Pin(ports[port][1])

        self.smg = TM1637(clk=clk, dio=dio)

    def show(self, string):
        self.smg.show(str(string))

    def showscroll(self, string):
        self.smg.scroll(str(string))


class radio:
    def __init__(self, code):
        from _educore.radio import Radio
        self.r = Radio(code)

    def send(self, content):
        self.r.send(content)

    def on(self):
        self.r.on()

    def off(self):
        self.r.off()

    def setcb(self, func):
        self.r.setcb(func)

    def recv(self):
        return self.r.recv()
