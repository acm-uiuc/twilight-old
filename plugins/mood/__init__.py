import colorsys


class Plugin:

    def __init__(self):
        self.hue = 0.0
        self.tile_matrix = []

    def ready(self):
        return True

    def setTileMatrix(self, tile_matrix):
        self.tile_matrix = tile_matrix

    def getNextFrame(self):
        self.hue += 0.0025
        red, green, blue = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        red = int(255 * red)
        green = int(255 * green)
        blue = int(255 * blue)
        frame = {}
        for tile in self.tile_matrix:
            if tile is not None:
                frame[tile["unit"]] = (red, green, blue)
        return frame
