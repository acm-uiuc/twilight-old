class Filter:

    def __init__(self):
        pass

    def active(self):
        """Defines whether this filter will affect the current frame"""
        return False

    def applyToFrame(self, tile_matrix):
        """Receives as input one frame of color data in a dictionary
        where unit IDs map to either a tuple or a list of tuples. Returns
        filtered color data in the same format."""
        raise NotImplementedError
