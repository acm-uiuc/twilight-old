import random
from plugin_base import Plugin


class EpilepsyPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)

    def ready(self):
        return True

    def getNextFrame(self):
        """Returns a dict of the form unit_id:(r,g,b)"""
        red = random.randint(0, 254)
        green = random.randint(0, 254)
        blue = random.randint(0, 254)
        frame = {}
        for tile in self.tile_matrix:
            if tile is not None:
                frame[tile["unit"]] = (red, green, blue)
        return frame
