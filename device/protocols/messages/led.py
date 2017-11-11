import msgs

class LEDMessages(msgs.Message):
    def __init__(self, color):
        #TODO: Right now we will only support solid colors, need to change this later 
        self.color = color
        self.type = MsgType.LED

    def serialize(self):
        return "{}:{},{},{}".format(self.type.name, self.color[0], self.color[1], self.color[2])

    def deserialize(str):
        if str.startswith("LED:"):
            components = (str[len("LED:"):]).split(,)
            color = tuple(compoennts[0],compoennts[1],compoennts[2])
            return LEDMsg(color)
        else:
            raise ValueError