class Plugin:

    def __init__(self):
        self.tile_matrix = []

    def ready(self):
        return False

    def setTileMatrix(self, tile_matrix):
        self.tile_matrix = tile_matrix

    def getNextFrame(self):
        raise NotImplementedError('getNextFrame not implemented.')
