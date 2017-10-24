import abc


class LEDFrame(abc.ABC):
    @abc.abstractmethod
    def init(self):
        '''
        Declare a new LED frame
        '''

    @abc.abstractmethod
    def serialize():
        '''
        Serialize the LED Frame into a string 
        '''



    