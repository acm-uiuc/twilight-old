// Contains EEPROM.read() and EEPROM.write()
#include <EEPROM.h>

// ID of the settings block
#define CONFIG_VERSION "ls1"

// Tell it where to store your config data in EEPROM
#define CONFIG_START 32


// Example settings structure
struct StoreStruct {
  // The variables of your settings
  uint32_t id;
  // This is for mere detection if they are your settings
  char version_of_program[4]; // it is the last variable of the struct
  // so when settings are saved, they will only be validated if
  // they are stored completely.
} settings = {
  // The default values
  1,
  CONFIG_VERSION
};


void load_config() {
  // To make sure there are settings, and they are YOURS!
  // If nothing is found it will use the default settings.
  if (//EEPROM.read(CONFIG_START + sizeof(settings) - 1) == settings.version_of_program[3] // this is '\0'
      EEPROM.read(CONFIG_START + sizeof(settings) - 2) == settings.version_of_program[2] &&
      EEPROM.read(CONFIG_START + sizeof(settings) - 3) == settings.version_of_program[1] &&
      EEPROM.read(CONFIG_START + sizeof(settings) - 4) == settings.version_of_program[0])
  { // reads settings from EEPROM
    for (unsigned int t=0; t<sizeof(settings); t++)
      *((char*)&settings + t) = EEPROM.read(CONFIG_START + t);
  } else {
    // settings aren't valid! will overwrite with default settings
    save_config();
  }
}

void save_config() {
  for (unsigned int t=0; t<sizeof(settings); t++)
  { // writes to EEPROM
    EEPROM.write(CONFIG_START + t, *((char*)&settings + t));
    // and verifies the data
    if (EEPROM.read(CONFIG_START + t) != *((char*)&settings + t))
    {
      // error writing to EEPROM
    }
  }
}


uint8_t blink_rate;
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  load_config();
  Serial.print(settings.id);
  if (settings.id == 2) {
      blink_rate = 10;
  } else if (settings.id == 5) {
      blink_rate = 100;
  } else if (settings.id == 6) {
      blink_rate = 1000;
  } else {
      blink_rate = 0;
  }
}

// the loop function runs over and over again forever
void loop() {
  //Serial.print(settings.id);
  if (settings.id == 6) {
     Serial1.write(blink_rate);
     Serial2.write(blink_rate);
  } else {
    blink_rate = Serial1.read();
    Serial.print(blink_rate);
  }
  
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(blink_rate);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(blink_rate);                       // wait for a second*/
}
