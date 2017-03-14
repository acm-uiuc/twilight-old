"""
Loads configurations from config file.
Please keep docstrings in sync with config.yaml
"""

import yaml

CONFIG_FILE_NAME = "config.yaml"
"""The name of the YAML file from which to get configuration."""

NUM_TILES_LENGTH = int()
"""The number of full tiles in the North-South span of the room."""

NUM_TILES_WIDTH = int()
"""The number of full tiles in the East-West span of the room."""

NUM_LEDS_PER_STRIP = int()
"""The number of RGB LEDS on each strip."""

CLAMP = int()
"""255, or 0xFF is being used a sentinel value in message strings sent to the
controllers. CLAMP then, represents the highest value that should be sent as
part of a color message."""

RATE_LIMIT_TIME = int()
"""Safe amount of time (milis) between consecutive writes to the same unit."""

SERIAL_RATE = int()
#TODO(wchill): write docstring for this.

DEBUG_MODE = True

UNIT_DETAILS = {}
"""Placeholder. This variable is being used as part of building UNITS."""

UNITS = [
    ((9, 6), "a", '/dev/ttyACM4'),
    ((5, 6), "b", '/dev/ttyACM1'),
    ((5, 2), "c", '/dev/ttyACM0'),
]


def load_config(globs):
    """Read file and set values"""
    config_dict = yaml.load(open(CONFIG_FILE_NAME, 'r'))
    for key in config_dict:
        print("\nASSIGNING VARS:")
        globs[key] = config_dict[key]
        print("key={} | globs.{} = config.{}".format(key, globs[key], config_dict[key]))

    # Special case of mapping details to units
    globs["UNITS"] = []
    for unit_id, details in globs["UNIT_DETAILS"].items():
        unit_position = (details["position_ns"], details["position_we"])
        unit_port = details["serial_port"]
        unit = (unit_position, unit_id, unit_port)
        globs["UNITS"].append(unit)

