

NUM_TILES_LENGTH = 15
"""The number of full tiles in the North-South span of the room."""

NUM_TILES_WIDTH = 10
"""The number of full tiles in the East-West span of the room."""

NUM_LEDS_PER_STRIP = 140
"""The number of RGB LEDS on each strip."""

SERIAL_RATE = 460800
#TODO(wchill): write docstring for this.

UNITS = [
    ((5, 2), "a", '/dev/ttyACM0'),
    ((5, 6), "b", '/dev/ttyACM1'),
    ((9, 6), "c", '/dev/ttyACM4'),
]
