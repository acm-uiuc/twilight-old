import time
from filter_base import Filter


class BrightnessFilter(Filter):

    def __init__(self):
        Filter.__init__(self)
        self.name = "Brightness Filter"
        self.parameters = {
            "brightness": 1.0
        }
        self.last_frame_time = 0

    def active(self):
        return time.time() - self.last_frame_time > 0.1

    def apply_to_frame(self, tile_matrix):
        output_matrix = {}
        for unit in tile_matrix:
            if isinstance(tile_matrix[unit], tuple):
                output_matrix[unit] = tuple([channel*self.parameters["brightness"] for channel in tile_matrix[unit]])
            else:
                unit_pixels = []
                for pixel in tile_matrix[unit]:
                    unit_pixels.append(tuple([channel*self.parameters["brightness"] for channel in pixel]))
                output_matrix[unit] = unit_pixels
        self.last_frame_time = time.time()
        return output_matrix


filter_plugin = BrightnessFilter
