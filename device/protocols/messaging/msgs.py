import abc

class msg(abc.ABC):
    @abc.abstractmethod
    def __init__(self, cfg):
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
        '''
        Serialize a message for transfer 
        '''
    
    @abc.abstractmethod
    def deserialize(str):
        '''
        deserialize a string for use in an application
        '''
