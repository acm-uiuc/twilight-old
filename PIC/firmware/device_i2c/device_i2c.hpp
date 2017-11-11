#ifndef DEVICE_I2C
#define DEVICE_I2C

#include "constants/directions.hpp"
#include "Arduino.h" 


//Send all messages to the device 
void recvd_msgs();
//Get messages to send to other devices
void msgs_to_be_sent();
//i2c thread
void handle_i2c_msgs();

void handle_i2c_msgs() {

}
//

#endif //DEVICE_I2C