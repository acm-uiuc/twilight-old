#include <EEPROM.h>
#include <FastLED.h>

#ifndef __AVR__
#include "TeensyID.h"
#endif

#define NUM_LEDS 140
#define DATA_PIN 6

// Wait until data is available in the serial receive buffer, then return one byte.
// WARNING: On Teensy, when using USB serial, Serial.available() may only return 1 despite
// more than one byte being available!
uint8_t blocking_serial_read() {
    while(Serial.available() == 0);
    return Serial.read();
}

// All commands sent to the microcontroller require a synchronization handshake.
const uint8_t handshake[] = {0xDE, 0xAD, 0xBE, 0xEF};

// LED framebuffer
CRGB leds[NUM_LEDS];

// Set up our function pointer typedef and table
typedef void (*Function) (void);

// Forward declarations
// TODO: Move these into separate files
void send_hardware_serial();
void display_frame();
void write_eeprom();
void read_eeprom();

const Function func_table[] = {
    // Command bytes specify which function to call.
    
    // 0x00
    send_hardware_serial,

    // 0x01
    display_frame,

    // 0x02
    write_eeprom,

    // 0x03
    read_eeprom
};

void send_hardware_serial() {
    // On Arduino, unique hardware IDs are unavailable.
    // Emulate a unique hardware ID by reading 4 bytes from EEPROM.
    uint8_t serial_id[4];
    #ifdef __AVR__
    serial_id[0] = EEPROM.read(0);
    serial_id[1] = EEPROM.read(1);
    serial_id[2] = EEPROM.read(2);
    serial_id[3] = EEPROM.read(3);
    #else
    // On Teensy, read 4 bytes of the Teensy hardware MAC
    teensySN(serial_id);
    #endif

    // Notify the connected computer of our hardware ID
    Serial.write(serial_id, sizeof(serial_id));
}

void display_frame() {
    // Read enough bytes to fill up our framebuffer, then update the LEDs.
    int bytes_read = 0;
    while(bytes_read < NUM_LEDS * 3) {
        bytes_read += Serial.readBytes(((uint8_t*) leds) + bytes_read, NUM_LEDS * 3 - bytes_read);
    }
    FastLED.show();
}

void write_eeprom() {
    // First byte sent specifies the starting address
    // Second byte sent specifies the number of bytes to write, up to 255
    // Subsequent bytes specify the data that shold be written
    uint8_t address = blocking_serial_read();
    uint8_t len = blocking_serial_read();

    for(uint8_t i = 0; i < len; i++) {
      uint8_t value = blocking_serial_read();
      EEPROM.write(address++, value);
    }
}

void read_eeprom() {
    // First byte sent specifies the starting address
    // Second byte sent specifies the number of bytes to read, up to 255
    uint8_t address = blocking_serial_read();
    uint8_t len = blocking_serial_read();

    uint8_t buf[256];
    for(uint8_t i = 0; i < len; i++) {
      buf[i] = EEPROM.read(address++);
    }
    Serial.write(buf, len);
}

void setup() {
    // Note: on Teensy the set baud rate has no effect
    // Communication is always performed at 12Mbps
    Serial.begin(921600);

    // Set up our LED framebuffer and light the LEDs rainbow so we know it's on
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    fill_rainbow(leds, NUM_LEDS, 222);
    FastLED.show();
}

void loop() {
    // Check for synchronization handshake
    bool valid_header = 1;    
    while(blocking_serial_read() != handshake[0]);
    for(int i = 1; i < sizeof(handshake); i++) {
        if(blocking_serial_read() != handshake[i]) {
            valid_header = 0;
            break;
        }
    }

    if(valid_header) {
        // We're synchronized, get the command byte and run the appropriate function
        uint8_t command = blocking_serial_read();

        if(command < (sizeof(func_table)/sizeof(func_table[0]))) {
            func_table[command]();
        }
    }
}
