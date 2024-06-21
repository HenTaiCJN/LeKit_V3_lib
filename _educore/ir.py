import time

from machine import Pin

from pins_const import ports


class IR:
    CODE = {
        162: "1", 98: "2", 226: "3", 34: "4", 2: "5", 194: "6", 224: "7", 168: "8", 144: "9", 152: "0",
        104: "*", 176: "#", 24: "up", 74: "down", 16: "left", 90: "right", 56: "ok"
    }

    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        self.s_pin = Pin(ports[port][0], Pin.IN, Pin.PULL_UP)

        self.irRecv = self.s_pin
        self.irRecv.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.__handler)  # 配置中断信息
        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0
        self.changed = False
        self.callback = None

    def __handler(self, source):
        """
        中断回调函数
        """
        thisComeInTime = time.ticks_us()

        # 更新时间
        curtime = time.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime

        if 8500 <= curtime <= 9500:
            self.ir_step = 1
            return

        if self.ir_step == 1:
            if 4000 <= curtime <= 5000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif 2000 <= curtime <= 3000:  # 长按重复接收
                self.ir_step = 3
                self.repeat += 1

        elif self.ir_step == 2:  # 接收4个字节
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start  # 记录最后ok的时间
                self.ir_step = 0
                self.__check_cmd()

        elif self.ir_step == 3:  # 重复
            if 500 <= curtime <= 650:
                self.repeat += 1

    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x + 1]
            byte4 <<= 1
            if 1800 <= t <= 2800:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code
        if self.callback is not None:
            self.callback()

    def setcb(self, function):
        self.callback = function

    def read(self):
        return self.CODE.get(self.cmd, None)
