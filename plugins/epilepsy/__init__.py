import random
import twilight


class Plugin:

    def __init__(self):
        self.unit_ids = twilight.get_all_unit_ids()

    def ready(self):
        return True

    def getNextFrame(sef):
        red = random.randint(0, 254)
        green = random.randint(0, 254)
        blue = random.randint(0, 254)
        for unit_id in self.unit_ids:
            twilight.interface.set_unit_color(unit_id, (red, green, blue))
