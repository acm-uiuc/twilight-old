class Plugin:

    def __init__(self):
        self.tile_matrix = []

    def ready(self):
        """Specifies whether this plugin is ready to return a frame."""
        return False

    def setTileMatrix(self, tile_matrix):
        """Update the tile matrix used by this plugin."""
        self.tile_matrix = tile_matrix

    def getNextFrame(self):
        """Returns one frame of color data in a dictionary where unit IDs
        map to either a tuple or a list of tuples. Single tuples imply that
        all LEDs in the panel should be set to that color."""
        raise NotImplementedError('getNextFrame not implemented.')
