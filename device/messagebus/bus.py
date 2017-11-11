import RPi.GPIO as GPIO
import smbus
from protocols import messages

PIC_ADDR = 0#I2C Address of the PIC
PIC_IRQ_PIN = 0#Pin of the IRQ 
PI_IRQ_PIN = 0

class MessageBus():
    def __init__(self):
        self.inbox = []
        self.outbox = []
        self.i2c = smbus.SMBus(0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIC_IRQ_PIN, GPIO.IN)
        GPIO.setup(PI_IRQ_PIN, GPIO.OUT)
        GPIO.add_event_detect(PIC_IRQ_PIN, GPIO.RISING)
        GPIO.add_event_detect(PI_IRQ_PIN, GPIO.RISING)

    def listen(self):
        while True:
             if GPIO.event_detected(PIC_IRQ_PIN): 
                try:
                    data_recv = self.i2c.read_i2c_block_data(PIC_ADDR, 0,15)
                    for i in range(len(data_recv)):
                        msg += chr(data_recv[i])
                    _msg = msg.split(';')
                    msg_struct = messages.deserialize(_msg[0],_msg[1])
                    self.inbox.append(msg_struct)
                except IOError:
                    pass
        return

    def write():
        for m in self.outbox:
            '''protocol for sending msgs over i2c'''

        return 

    def send_msg(self, msg):
        self.outbox.append(msg.serialize())
        return

    def recv_msgs(self):
        incomming_msgs = self.inbox
        self.inbox = []
        return incomming_msgs

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()