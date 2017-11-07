import RPi.GPIO as GPIO
import smbus

PIC_ADDR = #I2C Address of the PIC
PIC_IRQ_PIN = #Pin of the IRQ 
PI_IRQ_PIN =

class MessageBus():
    def __init__(self):
        '''Initiate connection to the PIC here'''
        self.bus = smbus.SMBus(1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIC_IRQ_PIN, GPIO.IN)
        GPIO.setup(PI_IRQ_PIN, GPIO.OUT)
        GPIO.add_event_detect(PIC_IRQ_PIN, GPIO.RISING)
        GPIO.add_event_detect(PI_IRQ_PIN, GPIO.RISING)


    def listen(self):
        while True:
             if GPIO.event_detected(PIC_IRQ_PIN): 
                try:
                    data_recv = i2c.read_i2c_block_data(slaveAddress, 0,15)
                    for i in range(len(data_recv)):
                        smsMessage += chr(data_recv[i])
                except IOError:
                    pass

    def write(self):
        

    def __exit__():
        GPIO.cleanup()