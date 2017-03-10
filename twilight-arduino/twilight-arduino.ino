#include <FastLED.h>

#define NUM_LEDS 140
#define DATA_PIN 6

CRGB leds[NUM_LEDS];
int num_bytes = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(460800);

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  fill_rainbow(leds, NUM_LEDS, 222);
  //fill_solid(leds, NUM_LEDS, CRGB(255, 0, 0));
}

void loop() {
  FastLED.show();

  while(Serial.read() != 0xFF);

  int bytesRead = 0;
  while(bytesRead < NUM_LEDS * 3) {
    bytesRead += Serial.readBytes(((uint8_t*)leds) + bytesRead, NUM_LEDS * 3 - bytesRead);
  }
}
