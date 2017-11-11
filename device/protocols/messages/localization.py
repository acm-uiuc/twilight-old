import msgs
from uuid import getnode as get_mac

class LocalizationMessage(msgs.Message):
    def __init__(self, ID, location, ttl=100, hops=0, origin_id=get_mac(), source=msgs.Source.SELF):
        self.ID = ID
        self.hops = hops
        self.ttl = ttl
        self.origin_id = origin_id
        self.location = location
        self.type = MessageType.LOC
        self.source = source 

    def serialize(self):
        return "{}:{},{},{},{},{}.{}".format(self.type.name, self.ID, self.location[0], self.location[1], self.hops, self.ttl, self.origin_id)

    def deserialize(str, source):
        if str.startswith("LOC:"):
            components = (str[len("LOC:"):]).split(,)
            ID = int(components[0])
            location = tuple(components[1], components[2])
            hops = components[3]
            ttl = components[4]
            origin_id = components[5]
            return LocalizationMsg(ID, location, ttl, hops, origin_id, source)
        else:
            raise ValueError