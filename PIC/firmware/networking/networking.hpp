#ifndef NETWORKING_H
#define NETWORKING_H

#include "Arduino.h" 
#include <ArduinoSTL.h>
#include "protocols/protocols.hpp"
#include "constants/directions.hpp"



void setup_networking();
void handle_msgs();
void multicast(char* msg);
void send_msg(char* msg);
std::vector<char*> recv_msgs();

class NetworkExchange {
    std::vector<char*> inbox;
    std::vector<char*> outbox;
};

NetworkExchange interconnect = NetworkExchange();

void setup_networking() {
    Serial1.begin(9600); //NORTHBOUND
    Serial2.begin(9600); //SOUTHBOUND
}

void multicast(char* msg) {
    Serial1.print(msg);
    Serial2.print(msg);
}

void handle_msgs() {
    //Get new messages from other nodes
    if (Serial1.available()){

        msg_ = strcat(msg, ';')
        interconnect.inbox.push_back(strcat(msg_, NORTH));
    }
    if (Serial2.available()){

        msg_ = strcat(msg, ';')
        interconnect.inbox.push_back(msg_, SOUTH);
    }

    //Send messages in outbox
    for (int i = 0; i < interconnect.outbox.length; i++) {
        multicast(interconnect.outbox[i]);
    }
    interconnect.outbox.clear();
    return;
}

void send_msg(char* msg) {
    interconnect.outbox.push_back(msg);
}

std::vector<std::pair<int,char*>> recv_msgs() {
    std::vector<char*> msgs = interconnect.inbox;
    interconnect.inbox.clear();
    return msgs;
}


#endif //NETWORKING_H