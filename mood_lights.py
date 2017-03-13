
import time
import colorsys
import twilight

hue = 0.0

while True:
    hue += 0.0025
    red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    red = int(255 * red)
    green = int(255 * green)
    blue = int(255 * blue)
    twilight.interface.set_all_unit_color((red, green, blue))
    time.sleep(0.1)
