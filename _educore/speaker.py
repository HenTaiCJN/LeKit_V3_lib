import time

import gc
from machine import Pin, PWM
from pins_const import ports
import _thread


class speaker:
    def __init__(self, port):
        if port is None:
            print("请指定端口号")
        self.pin = None
        self.is_stop = False

        self.pin = ports[port][0]

        s_pin = Pin(self.pin, Pin.OUT)

        self.pwm = PWM(s_pin)
        self.pwm.duty(0)

    def tone(self, freq, durl=150, duty=512):
        self.is_stop = True
        time.sleep_ms(1000)
        _thread.start_new_thread(self.tone_ex, [freq, durl, duty])

    def tone_ex(self, freq, durl=150, duty=512):
        self.is_stop = False
        if not isinstance(freq, list):
            freq = [freq]
        self.pwm.duty(duty)

        for i in freq:
            if self.is_stop:
                self.is_stop = False
                break
            self.pwm.freq(i)
            time.sleep_ms(durl)

        self.pwm.duty(0)
        gc.collect()

    def stop(self):
        self.is_stop = True
        self.pwm.duty(0)
