import time
from filter_base import Filter


class GreyscaleFilter(Filter):

    def __init__(self):
        Filter.__init__(self)
        self.last_frame_time = 0

    def active(self):
        return time.time() - self.last_frame_time > 0.1

    def applyToFrame(self, tile_matrix):
        output_matrix = {}
        for unit in tile_matrix:
            if isinstance(tile_matrix[unit], tuple):
                avg = sum(tile_matrix[unit])/3
                output_matrix[unit] = (avg, avg, avg)
            else:
                unit_pixels = []
                for pixel in tile_matrix[unit]:
                    avg = sum(pixel)/3
                    unit_pixels.append((avg, avg, avg))
                output_matrix[unit] = unit_pixels
        self.last_frame_time = time.time()
        return output_matrix


filter = GreyscaleFilter
