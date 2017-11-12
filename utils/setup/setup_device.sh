#!/bin/bash
sudo apt update
sudo apt install -y avrdude python-smbus i2c-tools
avrdude -v
cat /etc/avrdude.conf avr_programming_pins.conf > ~/avrdude_gpio.conf
echo -e "Setup done, make sure to enable I2C with raspi-config"