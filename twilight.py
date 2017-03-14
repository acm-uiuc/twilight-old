
import collections
import queue
import time
import threading
import serial

import config_loader


class Twilight:
    """Interface for writing to Twilight"""

    def __init__(self):
        """Creates a Twilight object based on the configurations in config.py.
        """
        self.tile_matrix = [
            [None] * NUM_TILES_WIDTH for i in range(NUM_TILES_LENGTH)]
        self.id_to_fd = {}
        self.id_to_queue = {}
        self.threads = {}
        self.rate_limit_dict = collections.defaultdict(int)
        self.debug_mode = DEBUG_MODE
        self.should_safety_block = False

        for unit in UNITS:
            self.tile_matrix[unit[0][0]][unit[0][1]] = unit[1]
            if not self.debug_mode:
                port = serial.Serial(unit[2], SERIAL_RATE)
                unit_queue = queue.Queue()

                self.id_to_fd[unit[1]] = port
                self.id_to_queue[unit[1]] = unit_queue
                self.threads[unit[1]] = threading.Thread(
                    target=self.update_lights_helper,
                    daemon=True,
                    args=(unit_queue, port)
                )
                unit_queue.put(b'\xFF' + b'\x00x00x00' * NUM_LEDS_PER_STRIP)
                self.threads[unit[1]].start()

            if self.debug_mode:
                # TODO: Write a visualizer.
                pass

    def update_lights_helper(self, unit_queue, port):
        # TODO: Move the rate limiter into this code
        while True:
            lights = unit_queue.get()
            while not unit_queue.empty():
                # Get most recent frame if there are extra frames.
                lights = unit_queue.get()
            port.write(lights)

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

    def write_time_unsafe(self, unit_id):
        """Checks if a write to a twilight unit is unsafe based on how much
        time has passed since the last write. Returns True if unsafe. Returns
        False if safe. Also records this time for the next call.
        """
        current_time_ms = int(time.time()*1000)

        if current_time_ms - self.rate_limit_dict[unit_id] < RATE_LIMIT_TIME:
            if not self.should_safety_block:
                return True
            time.sleep(0.001 * RATE_LIMIT_TIME)
            current_time_ms = int(time.time()*1000)

        self.rate_limit_dict[unit_id] = current_time_ms
        return False

    def write_to_unit(self, unit_id, colors):
        """Write colors to a Twilight unit's LED strip.
        This function lets you set each individual LED in the unit. This
        function also has a rate limitor that drops messages sent within
        RATE_LIMIT_TIME (see config) seconds of each other. The rate limitor
        can be set to blocking mode as well.

        Args:
            unit_id: The id of the Twilight unit you want to write to.
            colors: List of len 140 containing 3 Tuple of 0-254 rgb values.
                All color inputs will be clipped to [0, 254]
        """
        if len(colors) != NUM_LEDS_PER_STRIP:
            # TODO: raise a more meaningful exception.
            # TODO: review this 140 number.
            raise Exception("len(colors) != 140.")
        if self.write_time_unsafe(unit_id):
            return

        # Colors are input as RGB. However, our LEDs take RBG :/
        rbg_colors = [(col[0], col[2], col[1]) for col in colors]

        # Build the message and make sure all values are between 0 and CLAMP
        serialized_colors = list(sum(rbg_colors, ()))
        serialized_colors = [max(0, min(CLAMP, c)) for c in serialized_colors]
        message = b'\xFF' + bytes(serialized_colors)

        if self.debug_mode:
            # TODO: pass values to visualizer
            print("Debug mode not implemented. Returning.")
            return message

        self.id_to_queue[unit_id].put(message)

    def set_unit_color(self, unit_id, rgb):
        """Set all LEDS in a given unit to a specific color.
        See write_to_unit() docs for details on rate limiting behavior.

        Args:
            unit_id: The id of the Twilight unit you want to write to.
            rgb: 3 Tuple containing 0-255 values for rgb color.
        """

        self.write_to_unit(unit_id, [rgb]*140)

    def set_all_unit_color(self, rgb):
        """Sets all units to the same color.
        See write_to_unit() docs for details on rate limiting behavior.

        Args:
            rgb: 3 Tuple containing 0-255 values for rgb color.
        """
        unit_ids = get_all_unit_ids()
        for unit_id in unit_ids:
            self.set_unit_color(unit_id, rgb)

config_loader.load_config(globals())
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


def set_should_safety_block_state(state):
    """Set whether your preference for the rate limiting behavior. Setting
    this to TRUE will cause writes to sleep the minimum safety time.
    Setting it to FALSE will cause writes to return immediately without
    doing anything if safety time is violated.

    False by default."""
    interface.should_safety_block = state


print(interface)
