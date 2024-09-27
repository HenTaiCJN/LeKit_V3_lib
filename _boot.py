import gc
import os
from flashbdev import bdev
import ssd1306fontFile

try:
    if bdev:
        os.mount(bdev, "/")
except OSError:
    import inisetup

    vfs = inisetup.setup()

gc.collect()
with open("boot.py", "w") as f:
    f.write(
"""\
from educore import oled
import brownout
brownout.disable()
oled.oled.displayclear()
oled.oled.displaytxtauto('LeKit-V3', 24, 16)
oled.oled.displaytxtauto('2024-9-27', 24, 32)
oled.oled.displayshow()
"""
    )
if 'main.py' not in os.listdir('/'):
    with open("main.py", "w") as f1:
        f1.write('')