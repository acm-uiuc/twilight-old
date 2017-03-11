
from config import *
import serial


class Twilight:
    """Interface for writing to Twilight"""

    def __init__(self, debug_mode = True):
        """Creates a Twilight object based on the configurations in config.py.
        """
        self.tile_matrix = [[None] * NUM_TILES_WIDTH for i in range(NUM_TILES_LENGTH)]
        self.serial_fds = {}
        for unit in UNITS:
            self.tile_matrix[unit[0][0]][unit[0][1]] = unit[1]
            if not debug_mode:
                self.serial_fds[unit[1]] = serial.Serial(unit[2], SERIAL_RATE)
            if debug_mode:
                # TODO: Create a visualizer and write to that visualizer.
                pass


    def __repr__(self):
        """Returns a string representation of the layout of Twilight."""
        result = ""
        for row in self.tile_matrix:
            for tile in row:
                if tile is None:
                    result += "_ "
                else:
                    result += tile + " "
            result += "\n"
        return result

    def write_to_unit(self, unit_id, colors):
        """Write colors to a Twilight unit's LED strip.
        This function lets you set each individual LED in the unit.

        Args:
            unit_id: The id of the Twilight unit you want to write to.
            colors: A 140 length list of 3-tuples for colors.
        """

        if len(colors) != NUM_LEDS_PER_STRIP:
            # TODO: raise a more meaningful exception.
            # TODO: review this 140 number.
            raise Exception("len(colors) != 140.")

        print("writing to serial")



matrix = Twilight()
print(matrix)