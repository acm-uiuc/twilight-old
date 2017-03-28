class Filter:

    def __init__(self):
        self.name = "Unnamed Filter"
        self.parameters = {}

    def active(self):
        """Defines whether this filter will affect the current frame"""
        return False

    def apply_to_frame(self, tile_matrix):
        """Receives as input one frame of color data in a dictionary
        where unit IDs map to either a tuple or a list of tuples. Returns
        filtered color data in the same format or None to drop frame."""
        raise NotImplementedError

    def get_params(self):
        """Returns the parameters and current values for this filter as a
        dictionary."""
        return self.parameters

    def set_param(self, param, value):
        """Sets the value of the parameter param to value, and raises a
        KeyError if the parameter supplied is invalid."""
        if param in self.parameters:
            self.parameters[param] = value
        else:
            raise KeyError("{} is not a valid parameter for plugin {}".format(param, self.name))