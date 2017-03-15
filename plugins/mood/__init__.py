import colorsys
from plugin_base import Plugin


class MoodLightPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        self.hue = 0.0

    def ready(self):
        return True

    def getNextFrame(self):
        self.hue += 0.0025
        red, green, blue = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        red = int(255 * red)
        green = int(255 * green)
        blue = int(255 * blue)
        frame = {}
        for row in self.tile_matrix:
            for tile in row:
                if tile is not None:
                    frame[tile["unit"]] = (red, green, blue)
        return frame


plugin = MoodLightPlugin
