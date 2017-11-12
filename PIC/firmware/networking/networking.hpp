#ifndef NETWORKING_H
#define NETWORKING_H

#include "Arduino.h" 
#include <ArduinoSTL.h>
//#include "protocols/protocols.hpp"
#include "../constants/directions.hpp"



void setup_networking();
void handle_msgs();
void multicast(String msg);
void send_msg(String msg);
std::vector<String> recv_msgs();

typedef struct NetworkExchange_struct {
    std::vector<String> inbox;
    std::vector<String> outbox;
} NetworkExchange ;

NetworkExchange interconnect = NetworkExchange();

void setup_networking() {
    Serial.begin(9600); //DEBUGGING
    Serial1.begin(9600); //NORTHBOUND
    Serial2.begin(9600); //SOUTHBOUND
}

void multicast(String msg) {
    Serial.println(String(msg + ';' + String(SELF)));
    Serial1.print(msg);
    Serial2.print(msg);
}

void handle_msgs() {
    //Get new messages from other nodes
    Serial.println("Checking for messages");
    if (Serial1.available()) {
        Serial.println("Looking to Read from NORTHBOUND Serial");
        String msg = Serial1.readString();
        Serial.println(String(msg + ';' + String(NORTH)));
        interconnect.inbox.push_back(String(msg + ';' + String(NORTH)));
    }
    if (Serial2.available()) {
        Serial.println("Looking to Read from SOUTHBOUND Serial");
        String msg = Serial2.readString();
        Serial.println(String(msg + ';' + String(SOUTH)));
        interconnect.inbox.push_back(String(msg + ';' + String(SOUTH)));
    }

    //Send messages in outbox
    for (int i = 0; i < interconnect.outbox.size(); i++) {
        multicast(interconnect.outbox[i]);
    }
    interconnect.outbox.clear();
    return;
}

void send_msg(String msg) {
    interconnect.outbox.push_back(msg);
}

std::vector<String> recv_msgs() {
    std::vector<String> msgs = interconnect.inbox;
    interconnect.inbox.clear();
    return msgs;
}


#endif //NETWORKING_H