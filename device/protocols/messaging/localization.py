import msgs

class LocalizationMsg(msgs.msg):
    def __init__(self, ID, location):
        self.ID = ID
        self.location = location 

    def serialize(self):
        return "localization:{},{}".format(self.ID, self.location)

    def deserialize(str):
        if str.startswith("localization:"):
            components = (str[len("localization:"):]).split(,)
            ID = int(components[0])
            location = tuple(compoennts[1])
            return LocalizationMsg(ID, location)
        else:
            raise ValueError