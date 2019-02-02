DEVICE     = atmega328p
CLOCK      = 16000000
# PROGRAMMER = usbasp
PROGRAMMER = arduino
PORT	  	 = /dev/ttyACM1
BAUD       = 115200
FILE    	 = main
COMPILE    = avr-gcc -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(DEVICE)

all: build upload

8mhz-internal:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0xe2:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

1mhz-internal:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0x62:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

build:
	$(COMPILE) -c light_ws2812.c -o light_ws2812.o
	$(COMPILE) -c main.c -o main.o
	$(COMPILE) -o main.elf main.o light_ws2812.o
	avr-objcopy -j .text -j .data -O ihex main.elf main.hex
	avr-size --format=avr --mcu=$(DEVICE) main.elf

upload:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD) -U flash:w:$(FILE).hex:i

clean:
	rm main.o
	rm main.elf
	rm main.hex
	rm light_ws2812.o
