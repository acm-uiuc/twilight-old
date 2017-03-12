import time
import colorsys
import twilight
from random import randint

unit_ids = twilight.get_all_unit_ids()

hue = 0.0

while True:

    for unit_id in unit_ids:
        red = randint(0,255)
        green = randint(0, 255)
        blue = randint(0,255)
        rgb_tuple = (red, green, blue)
        twilight.interface.set_unit_color(unit_id, rgb_tuple)
    
    time.sleep(0.1)

