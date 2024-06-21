import time

from machine import Pin


class button:
    def __init__(self, ch=None):
        self._event_pressed = None
        self.last_time = time.time()

        self.s_pin = Pin(int(ch), mode=Pin.IN)

    def status(self):
        return self.s_pin.value()

    @property
    def event_pressed(self):
        return self._event_pressed

    @event_pressed.setter
    def event_pressed(self, callback):
        self._event_pressed = callback
        self.s_pin.irq(trigger=Pin.IRQ_RISING, handler=self.callback)

    def callback(self, e):
        if self._event_pressed is not None:
            self._event_pressed()