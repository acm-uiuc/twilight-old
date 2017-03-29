import signal
import twilight

unit_ids = twilight.get_all_unit_ids()

for unit_id in unit_ids:
    twilight.interface.set_unit_color(unit_id, (0, 0, 0))

signal.signal(signal.SIGINT, signal.default_int_handler)

led_counts = {unit_id: 0 for unit_id in unit_ids}

for unit_id in unit_ids:
    print('Testing unit %s' % unit_id)

    led_count = 0

    while True:
        colors = [(0, 0, 0) for i in range(140)]
        colors[led_count] = (254, 254, 254)
        try:
            twilight.interface.write_to_unit(unit_id, colors)
            led_count += 1
            input('Current LED: LED #%d' % led_count)
        except KeyboardInterrupt:
            print('Stopped at LED #%d' % led_count)
            break

    led_counts[unit_id] = led_count
    print('')

print(led_counts)
