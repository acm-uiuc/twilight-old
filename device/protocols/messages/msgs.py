import abc
from enum import Enum
import localization
import led

class MessageType(Enum):
    LOC = 1
    LED = 2
    DATA = 3

class Source(Enum):
    SELF = 0
    NORTH = 1
    SOUTH = 2
    #EAST = 3
    #WEST = 4

class Message(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        '''
        Instanciate a message
        '''
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    @abc.abstractmethod
    def serialize(self):
        pass

    @staticmethod
    def deserialize(str, source=None):
        '''
        deserialize a string for use in an application
        '''
        if str.startswith("LED:"):
            return led.LEDMessage.deserialize(str)
        elif str.startswith("LOC:"):
            return localization.LocalizationMessage.deserialize(str, source)
        else:
            raise ValueError
