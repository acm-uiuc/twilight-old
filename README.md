# Twilight

[![Join the chat at https://gitter.im/acm-uiuc/twilight](https://badges.gitter.im/acm-uiuc/twilight.svg)](https://gitter.im/acm-uiuc/twilight?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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
