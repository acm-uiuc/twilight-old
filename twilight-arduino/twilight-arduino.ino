#include <EEPROM.h>
#include <FastLED.h>

#ifndef __AVR__
#include "TeensyID.h"
#endif

#define NUM_LEDS 140
#define DATA_PIN 6

const uint8_t handshake[] = {0xDE, 0xAD, 0xBE, 0xEF};

CRGB leds[NUM_LEDS];

typedef void (*Function) (void);

void send_hardware_serial();
void display_frame();
void write_eeprom();

uint8_t blocking_serial_read() {
    while(Serial.available() == 0);
    return Serial.read();
}

const Function func_table[] = {
    // 0x00
    send_hardware_serial,

    // 0x01
    display_frame,

    // 0x02
    write_eeprom
};

void send_hardware_serial() {
    uint8_t serial_id[4];
    #ifdef __AVR__
    serial_id[0] = EEPROM.read(0);
    serial_id[1] = EEPROM.read(1);
    serial_id[2] = EEPROM.read(2);
    serial_id[3] = EEPROM.read(3);
    #else
    teensySN(serial_id);
    #endif

    Serial.write(serial_id, sizeof(serial_id));
}

void display_frame() {
    int bytes_read = 0;
    while(bytes_read < NUM_LEDS * 3) {
        bytes_read += Serial.readBytes(((uint8_t*) leds) + bytes_read, NUM_LEDS * 3 - bytes_read);
    }
    FastLED.show();
}

void write_eeprom() {
    uint8_t address = blocking_serial_read();
    uint8_t value = blocking_serial_read();

    EEPROM.write(address, value);
}

void setup() {
    // Note: on Teensy the set baud rate has no effect
    // Communication is always performed at 12Mbps
    Serial.begin(460800);

    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    fill_rainbow(leds, NUM_LEDS, 222);
    FastLED.show();
}

void loop() {
    bool valid_header = 1;    
    while(blocking_serial_read() != handshake[0]);
    for(int i = 1; i < sizeof(handshake); i++) {
        if(blocking_serial_read() != handshake[i]) {
            valid_header = 0;
            break;
        }
    }

    if(valid_header) {
        uint8_t command = blocking_serial_read();

        if(command < 3) {
            func_table[command]();
        }
    }
}
