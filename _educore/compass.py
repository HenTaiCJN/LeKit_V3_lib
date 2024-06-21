from machine import Pin, SoftI2C,I2C

from pins_const import ports
from qmc5883l_micropython import qmc5883l


class qmc5883:
    def __init__(self, port=None):
        if port is None:
            print("请指定端口号")

        scl = Pin(ports[port][0])
        sda = Pin(ports[port][1])

        i2c = SoftI2C(sda=sda, scl=scl)

        self.qmc = qmc5883l.QMC5883L(i2c)

    def adjust(self):
        print('adjusting...')
        self.qmc.calibrate(5)
        print('adjust success')

    def direction(self):
        x, y, z, t = self.qmc.read_scaled()

        return self.qmc.get_angle(x, y) % 360

    def getx(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_x

    def gety(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_y

    def getz(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_z
