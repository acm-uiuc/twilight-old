class Plugin:

    def __init__(self):
        self.name = "Unnamed Plugin"
        self.tile_matrix = []
        self.parameters = {}

    def ready(self):
        """Specifies whether this plugin is ready to return a frame."""
        return False

    def set_tile_matrix(self, tile_matrix):
        """Update the tile matrix used by this plugin."""
        self.tile_matrix = tile_matrix

    def get_next_frame(self):
        """Returns one frame of color data in a dictionary where unit IDs
        map to either a tuple or a list of tuples. Single tuples imply that
        all LEDs in the panel should be set to that color."""
        raise NotImplementedError('getNextFrame not implemented.')

    def get_params(self):
        """Returns the parameters and current values for this plugin as a
        dictionary."""
        return self.parameters

    def set_param(self, param, value):
        """Sets the value of the parameter param to value, and raises a
        KeyError if the parameter supplied is invalid."""
        if param in self.parameters:
            self.parameters[param] = value
        else:
            raise KeyError("{} is not a valid parameter for plugin {}".format(param, self.name))