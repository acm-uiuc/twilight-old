#!/bin/bash
sudo apt update
sudo apt install -y avrdude
avrdude -v
cat /etc/avrdude.conf avr_programming_pins.conf > ~/avrdude_gpio.conf
