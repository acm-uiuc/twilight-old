#ifndef NETWORKING_H
#define NETWORKING_H

#include "Arduino.h" 

void setup_networking();
void send_msg(char* msg);
void recv_msg();

void setup_networking() {
    Serial1.begin(9600);
    Serial2.begin(9600);
 }



#endif //NETWORKING_H