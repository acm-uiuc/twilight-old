import collections
import queue
import time
import threading
import serial

from config_loader import config_loader

"""The name of the YAML file from which to get configuration."""
CONFIG_FILE_NAME = 'config.yml'

"""Synchronization header to send to the Teensy on each command."""
SYNC_HEADER = b'\xDE\xAD\xBE\xEF'

"""Command byte that tells the Teensy to display a frame."""
CMD_DISPLAY_FRAME = SYNC_HEADER + b'\x01'

"""Number of frames to use for FPS calculation"""
FPS_FRAME_COUNT = 120

default_config = {
    # The number of full tiles in the North-South span of the room.
    'NUM_TILES_LENGTH': 15,

    # The number of full tiles in the East-West span of the room.
    'NUM_TILES_WIDTH': 10,

    # The number of RGB LEDS on each strip.
    'NUM_LEDS_PER_STRIP': 140,

    # Safe amount of time (milis) between consecutive writes to the same unit.
    'RATE_LIMIT_TIME': 10,

    # The rate at which to write to the serial port (in bits per second).
    'SERIAL_RATE': 460800,

    # Enable debug mode.
    'DEBUG_MODE': True,

    # Information about Twilight panel units.
    'UNITS': {},

    # Folder for holding plugins
    'PLUGINS_FOLDER': '/plugins/',

    # Default program length, in seconds
    'PLUGIN_CYCLE_LENGTH': 30
}


config_loader.register_config('twilight', CONFIG_FILE_NAME, default_config)
config = config_loader.load_config('twilight')


class Twilight:
    """Interface for writing to Twilight"""

    def __init__(self):
        """Creates a Twilight object based on the configurations in config.py.
        """
        self.id_to_fd = {}
        self.id_to_queue = {}
        self.threads = {}
        self.rate_limit_dict = collections.defaultdict(int)
        self.should_safety_block = False

        self.plugin_frame_times = {}
        self.rendered_frame_times = {}
        self.generated_frame_times = {}

        self.load_tile_matrix()

        if config['DEBUG_MODE']:
            # TODO: Write a visualizer.
            pass

    def load_tile_matrix(self):
        # Close existing file descriptors and threads
        for key in self.id_to_queue:
            self.id_to_queue[key].put(None)

        self.tile_matrix = [
            [None] * config['NUM_TILES_WIDTH'] for i in range(config['NUM_TILES_LENGTH'])]

        for unit in config['UNITS']:
            north_south, west_east = config['UNITS'][unit]['north_south'], config['UNITS'][unit]['west_east']
            my_unit = {
                'unit': unit,
                'position_ns': north_south,
                'position_we': west_east,
                'serial_port': config['UNITS'][unit]['serial_port']
            }
            self.tile_matrix[north_south][west_east] = my_unit

            if not config['DEBUG_MODE']:
                port = serial.Serial(my_unit['serial_port'], config['SERIAL_RATE'])
                unit_queue = queue.Queue()
                rendered_frame_times = collections.deque(maxlen=FPS_FRAME_COUNT)
                generated_frame_times = collections.deque(maxlen=FPS_FRAME_COUNT)
                # Set up the threads writing data to the serial port.
                self.id_to_fd[unit] = port
                self.id_to_queue[unit] = unit_queue
                self.rendered_frame_times[unit] = rendered_frame_times
                self.generated_frame_times[unit] = generated_frame_times
                self.threads[unit] = threading.Thread(
                    target=self.update_lights_helper,
                    daemon=True,
                    args=(unit_queue, port, rendered_frame_times)
                )

                # Turn off all the LEDs.
                unit_queue.put(CMD_DISPLAY_FRAME + b'\x00x00x00' * config['NUM_LEDS_PER_STRIP'])
                self.threads[unit].start()

    def update_lights_helper(self, unit_queue, port, frame_times):
        # TODO: Move the rate limiter into this code
        while True:
            lights = unit_queue.get()

            # Check for sentinel value and close serial port if needed.
            if lights is None:
                port.close()
                return

            while not unit_queue.empty():
                # Get most recent frame if there are extra frames.
                lights = unit_queue.get()
                if lights is None:
                    port.close()
                    return

            # Write the frame.
            port.write(lights)

            # Record the time frame was rendered for FPS calculation.
            frame_times.append(time.time())

    def __repr__(self):
        """Returns a string representation of the layout of Twilight."""
        result = ''
        for row in self.tile_matrix:
            for tile in row:
                if tile is None:
                    result += '_ '
                else:
                    result += tile['unit'] + ' '
            result += '\n'
        return result

    def write_time_unsafe(self, unit_id):
        """Checks if a write to a twilight unit is unsafe based on how much
        time has passed since the last write. Returns True if unsafe. Returns
        False if safe. Also records this time for the next call.
        """
        current_time_ms = int(time.time()*1000)

        if current_time_ms - self.rate_limit_dict[unit_id] < config['RATE_LIMIT_TIME']:
            if not self.should_safety_block:
                return True
            time.sleep(0.001 * config['RATE_LIMIT_TIME'])
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
        if len(colors) != config['NUM_LEDS_PER_STRIP']:
            # TODO: raise a more meaningful exception.
            # TODO: review this 140 number.
            raise Exception("Got %d colors, expected %d." % (len(colors), config['NUM_LEDS_PER_STRIP']))

        # Record the time this frame was generated for FPS calculation
        self.generated_frame_times[unit_id].append(time.time())

        if self.write_time_unsafe(unit_id):
            return

        # Colors are input as RGB. However, our LEDs take RBG :/
        rbg_colors = [(col[0], col[2], col[1]) for col in colors]

        # Build the message
        serialized_colors = list(sum(rbg_colors, ()))
        message = CMD_DISPLAY_FRAME + bytes(serialized_colors)

        if config['DEBUG_MODE']:
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
        unit_ids = self.get_all_unit_ids()
        for unit_id in unit_ids:
            self.set_unit_color(unit_id, rgb)

    def get_unit_id(self, position):
        """Takes a (North-South, East-West) position and returns the id of the
        twilight unit at that location. Returns None if there is no unit there.
        """
        return self.tile_matrix[position[0]][position[1]]

    def get_all_unit_ids(self):
        """Returns a list of all twilight unit ids."""
        return [unit for unit in config['UNITS']]

    def set_should_safety_block_state(self, state):
        """Set whether your preference for the rate limiting behavior. Setting
        this to TRUE will cause writes to sleep the minimum safety time.
        Setting it to FALSE will cause writes to return immediately without
        doing anything if safety time is violated.

        False by default."""
        self.should_safety_block = state

    def get_generated_fps(self):
        """Get the FPS of generated frames for each unit."""
        fps = {}
        for unit_id in self.generated_frame_times:
            unit_deque = self.generated_frame_times[unit_id]
            if len(unit_deque) > 1:
                fps[unit_id] = len(unit_deque) / (unit_deque[-1] - unit_deque[0])
            else:
                fps[unit_id] = 0

        return fps

    def get_rendered_fps(self):
        """Get the FPS of actually rendered frames for each unit."""
        fps = {}
        for unit_id in self.rendered_frame_times:
            unit_deque = self.rendered_frame_times[unit_id]
            if len(unit_deque) > 1:
                fps[unit_id] = len(unit_deque) / (unit_deque[-1] - unit_deque[0])
            else:
                fps[unit_id] = 0

        return fps

    def clear_fps_data(self):
        """Clear the deques containing frame times."""
        for unit_id in self.rendered_frame_times:
            self.rendered_frame_times[unit_id].clear()
            self.generated_frame_times[unit_id].clear()


interface = Twilight()
"""This is your interface to Twilight."""


print(interface)
