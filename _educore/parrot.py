import time

from machine import Pin, PWM

from pins_const import ports


def linear_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class parrot:
    M1 = 1
    M2 = 2

    def __init__(self, port):
        if port is None:
            print("请指定端口号")

        self.in0 = ports[port][0]
        self.in1 = ports[port][1]

        self.motor_pin1 = None
        self.motor_pin2 = None
        self.motor_pwm = None
        self.speed = None
        self.speed_old = None

        self.init_external_motor()

    def init_external_motor(self):
        if isinstance(self.in0, int):
            self.motor_pin1 = Pin(self.in0, Pin.OUT)
        else:
            self.motor_pin1 = self.in0.get_pin()

        if isinstance(self.in1, int):
            self.motor_pin2 = Pin(self.in1, Pin.OUT)
        else:
            self.motor_pin2 = self.in1.get_pin()

        self.motor_pwm = PWM(self.motor_pin2)
        # 刚初始化时不转动
        self.motor_pin1.value(0)
        self.motor_pwm.duty(0)

    def set_speed(self, speed=None):

        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        if self.speed_old == speed:
            return
        self.speed = speed
        self.speed_old = speed
        self.updata_onboard()

    def updata_onboard(self):
        self.motor_pwm.deinit()
        self.motor_pwm = PWM(self.motor_pin2, freq=50000)
        if self.speed > 0:
            self.motor_pin1.value(1)
            self.motor_pwm.duty(0)
            time.sleep_ms(10)
            mapped_value = linear_map(self.speed, 1, 100, 25, 96)
            self.motor_pwm.duty(int((100 - mapped_value) * 10.23))
        elif self.speed < 0:
            self.motor_pin1.value(0)
            self.motor_pwm.duty(1023)
            time.sleep_ms(10)
            mapped_value = linear_map(self.speed, -1, -100, -75, -100)
            self.motor_pwm.duty(int(-mapped_value * 10.23))
        else:
            self.motor_pin1.value(0)
            self.motor_pwm.duty(0)
