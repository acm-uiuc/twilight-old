
from config import *
import serial


class Twilight:
    """Interface for writing to Twilight"""

    def __init__(self):
        """Creates a Twilight object based on the configurations in config.py.
        """
        self.tile_matrix = [[None] * NUM_TILES_WIDTH for i in range(NUM_TILES_LENGTH)]
        self.id_to_fd = {}
        self.debug_mode = DEBUG_MODE

        for unit in UNITS:
            self.tile_matrix[unit[0][0]][unit[0][1]] = unit[1]
            if not self.debug_mode:
                self.id_to_fd[unit[1]] = serial.Serial(unit[2], SERIAL_RATE)
            if self.debug_mode:
                # TODO: Create a visualizer and write to that visualizer.
                pass

    def __repr__(self):
        """Returns a string representation of the layout of Twilight."""
        result = ''
        for row in self.tile_matrix:
            for tile in row:
                if tile is None:
                    result += '_ '
                else:
                    result += tile + ' '
            result += '\n'
        return result

    def write_to_unit(self, unit_id, colors):
        """Write colors to a Twilight unit's LED strip.
        This function lets you set each individual LED in the unit.

        Args:
            unit_id: The id of the Twilight unit you want to write to.
            colors: List of len 140 containing 3 Tuple of 0-255 rgb values.
        """
        if len(colors) != NUM_LEDS_PER_STRIP:
            # TODO: raise a more meaningful exception.
            # TODO: review this 140 number.
            raise Exception("len(colors) != 140.")

        rbg_colors = [(col[0], col[2], col[1]) for col in colors]
        # Colors are input as RGB. However, our LEDs take RBG :/

        serialized_colors = list(sum(rbg_colors, ()))
        message = b'\xFF' + bytes(serialized_colors)

        if self.debug_mode:
            # TODO: pass values to visualizer
            print("Debug mode not implemented. Returning.")
            return message

        self.id_to_fd[unit_id].write(message)

    def set_unit_color(self, unit_id, rgb):
        """Set all LEDS in a given unit to a specific color.

        Args:
            unit_id: The id of the Twilight unit you want to write to.
            colors: 3 Tuple containing 0-255 values for rgb color.
        """

        self.write_to_unit(unit_id, [rgb]*140)


interface = Twilight()
"""This is your interface to Twilight."""


def get_unit_id(position):
    """Takes a (North-South, East-West) position and returns the id of the
    twilight unit at that location. Returns None if there is no unit there.
    """
    return interface.tile_matrix[position[1]][position[0]]


def get_all_unit_ids():
    """Returns a list of all twilight unit ids."""
    return [unit[1] for unit in UNITS]

print(interface)
