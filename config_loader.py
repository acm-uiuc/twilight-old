"""
Loads configurations from config file and sets up 
"""

import yaml

CONFIG_FILE_NAME = "config.yaml"
with open(CONFIG_FILE_NAME, 'r') as config_file:
    config = yaml.load(config_file)

print(config)

NUM_TILES_LENGTH = config[]
"""The number of full tiles in the North-South span of the room."""

NUM_TILES_WIDTH = 10
"""The number of full tiles in the East-West span of the room."""

NUM_LEDS_PER_STRIP = 140
"""The number of RGB LEDS on each strip."""

CLAMP = 254
"""255, or 0xFF is being used a sentinel value in message strings sent to the
controllers. CLAMP then, represents the highest value that should be sent as
part of a color message."""

RATE_LIMIT_TIME = 100
"""Safe amount of time (milis) between consecutive writes to the same unit."""

SERIAL_RATE = 460800
#TODO(wchill): write docstring for this.

DEBUG_MODE = True

UNITS = [
    ((9, 6), "a", '/dev/ttyACM4'),
    ((5, 6), "b", '/dev/ttyACM1'),
    ((5, 2), "c", '/dev/ttyACM0'),
]
