import time
import colorsys
import twilight


class Plugin:
    
    def __init__(self):
        self.hue = 0.0

    def ready(self):
        return True

    def getNextFrame(self):
        self.hue += 0.0025
        red, green, blue = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        red = int(255 * red)
        green = int(255 * green)
        blue = int(255 * blue)
        twilight.interface.set_all_unit_color((red, green, blue))
