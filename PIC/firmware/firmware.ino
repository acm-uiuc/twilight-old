#include <ThreadController.h>
#include <StaticThreadController.h>
#include <Thread.h>
#include "networking/networking.hpp"
#include "led_driver/led_driver.hpp"

Thread LEDs = Thread();
Thread Network = Thread();
Thread DeviceI2C = Thread();
ThreadController ctrlr = ThreadController();

uint8_t counter = 0;

void setup() {
    
    //Setup LED Thread 
    setup_frame();
    LEDs.enabled = true;
    LEDs.setInterval(10);
    LEDs.onRun(update_frame);

    //Setup Network Thread
    /*setup_networking();
    Network.enabled = true;
    Network.setInterval(10);
    Network.onRun(handle_network_msgs);*/
    
    //DeviceI2C
    /*setup_i2c();
    DeviceI2C.enable = true;
    DeviceI2C.setInterval(10);
    DeviceI2C.onRun(handle_i2c_msgs);*/

    ctrlr.add(&LEDs);
    ctrlr.add(&Network);
    ctrlr.add(&DeviceI2C);
}

void loop() {
    ctrlr.run();
    if (counter % 3 == 0) {
        frame.SetColor(0,0,255);
    }
    
    else if (counter % 3 == 1) {
        frame.SetColor(0,255,0);
    }

    else {
        frame.SetColor(255,0,0);
    }
    counter++; 
}




