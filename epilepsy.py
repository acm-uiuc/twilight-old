
import random
import twilight

unit_ids = twilight.get_all_unit_ids()

while True:
    red = random.randint(0, 254)
    green = random.randint(0, 254)
    blue = random.randint(0, 254)
    for unit_id in unit_ids:
        twilight.interface.set_unit_color(unit_id, (red, green, blue))
