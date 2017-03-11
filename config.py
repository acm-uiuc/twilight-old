

NUM_TILES_LENGTH = 15
"""The number of full tiles in the North-South span of the room."""

NUM_TILES_WIDTH = 10
"""The number of full tiles in the East-West span of the room."""

NUM_LEDS_PER_STRIP = 140
"""The number of RGB LEDS on each strip."""

CLAMP = 254
"""Numbers sent in the message that are over CLAMP have special meanings."""

SERIAL_RATE = 460800
#TODO(wchill): write docstring for this.

DEBUG_MODE = True

UNITS = [
    ((9, 6), "a", '/dev/ttyACM4'),
    ((5, 6), "b", '/dev/ttyACM1'),
    ((5, 2), "c", '/dev/ttyACM0'),
]
