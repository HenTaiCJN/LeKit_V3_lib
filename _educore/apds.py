from apds9960 import uAPDS9960 as APDS9960
from apds9960 import const
from machine import SoftI2C, Pin

from pins_const import ports


class apds:
    def __init__(self,  port=None):
        if port is None:
            print("请指定端口号")

        scl = Pin(ports[port][0])
        sda = Pin(ports[port][1])

        self.bus = SoftI2C(sda=sda, scl=scl)
        self.apds = APDS9960(self.bus)
        self.dirs = {
            const.APDS9960_DIR_NONE: "none",
            const.APDS9960_DIR_LEFT: "left",
            const.APDS9960_DIR_RIGHT: "right",
            const.APDS9960_DIR_UP: "up",
            const.APDS9960_DIR_DOWN: "down",
            const.APDS9960_DIR_NEAR: "near",
            const.APDS9960_DIR_FAR: "far",
        }
        self.apds.setProximityIntLowThreshold(50)
        self.apds.enableGestureSensor()
        self.apds.enableProximitySensor()
        self.apds.enableLightSensor()
        self.res = ""

    def read(self):
        try:
            flag = self.apds.isGestureAvailable()
        except:
            return None
        if flag:
            try:
                motion = self.apds.readGesture()
                self.res = self.dirs.get(motion, "unknown")
                #             print("Gesture={}".format(self.dirs.get(motion, "unknown")))
                return self.res
            except:
                return None
        else:
            return None

    def readProximity(self):
        return self.apds.readProximity()

    def readLight(self):
        return self.apds.readAmbientLight()
