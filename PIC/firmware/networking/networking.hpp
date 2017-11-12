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
    Serial1.begin(9600); //NORTHBOUND
    Serial2.begin(9600); //SOUTHBOUND
}

void multicast(String msg) {
    Serial1.print(msg);
    Serial2.print(msg);
}

void handle_msgs() {
    //Get new messages from other nodes
    if (Serial1.available()){
        String msg = Serial1.readString();
        interconnect.inbox.push_back(String(msg + ';' + String(NORTH)));
    }
    if (Serial2.available()){
        String msg = Serial2.readString();
        interconnect.inbox.push_back(String(msg + ';' + String(NORTH)));
    }

    //Send messages in outbox
    for (int i = 0; i < interconnect.outbox.size(); i++) {
        multicast(interconnect.outbox[i]);
    }
    interconnect.outbox.clear();
    return;
}

void send_msg(char* msg) {
    interconnect.outbox.push_back(msg);
}

std::vector<String> recv_msgs() {
    std::vector<String> msgs = interconnect.inbox;
    interconnect.inbox.clear();
    return msgs;
}


#endif //NETWORKING_H