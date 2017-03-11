import time
import colorsys
import twilight

system = twilight.Twilight()
unit_ids = system.get_all_unit_ids()

hue = 0.0

while True:
    hue += 0.0025
    red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    red = int(255 * red)
    green = int(255 * green)
    blue = int(255 * blue)

    if red >= 255:
        red = 254
    elif red < 0:
        red = 0

    if green >= 255:
        green = 254
    elif green < 0:
        green = 0

    if blue >= 255:
        blue = 254
    elif blue < 0:
        blue = 0

    for unit_id in unit_ids:
        system.set_unit_color(unit_id, (red, green, blue))
        
    time.sleep(0.1)