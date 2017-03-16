import random
import time
from plugin_base import Plugin


class EpilepsyPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        self.last_frame_time = 0

    def ready(self):
        return True

    def getNextFrame(self):
        """Returns a dict of the form unit_id:(r,g,b)"""
        red = random.randint(0, 254)
        green = random.randint(0, 254)
        blue = random.randint(0, 254)
        frame = {}
        for row in self.tile_matrix:
            for tile in row:
                if tile is not None:
                    frame[tile["unit"]] = [(red, green, blue)] * 140
        self.last_frame_time = time.time()
        return frame


plugin = EpilepsyPlugin
