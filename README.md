# Twilight

Twilight is the ceiling lighting system at the ACM Office. 

Example usage:

```
import twilight

#we're going to set the first unit to red
rgb_tuple = (255,0,0)

unit_ids = twilight.get_all_unit_ids()
twilight.interface.set_unit_color(unit_ids[1], rgb_tuple)
```

We'll complete this README when the project is closer to being complete. 
