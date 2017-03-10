import time
import colorsys
import serial

sp1 = serial.Serial('/dev/ttyACM0', 460800)
sp2 = serial.Serial('/dev/ttyACM1', 460800)
sp3 = serial.Serial('/dev/ttyACM4', 460800)

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

    sp1.write(b'\xFF' + bytes(list(sum([(red, green, blue)] * 140, ()))))
    sp2.write(b'\xFF' + bytes(list(sum([(red, green, blue)] * 140, ()))))
    sp3.write(b'\xFF' + bytes(list(sum([(red, green, blue)] * 140, ()))))

    time.sleep(0.1)
