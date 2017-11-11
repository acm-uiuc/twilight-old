from .. import messages
from ..messages import LocalizationMessage
from ....messagebus import MessageBus
from uuid import getnode as get_mac


class Location():
    def __init__(self, message_bus):
        self.ID = get_mac()
        self.locale = (0,0)
        self.assignment_dist = 0
        self.message_bus = message_bus
        self.origin_id = get_mac()

        propogate_loc = LocalizationMessage(self.ID, self.locale, 100, 0 self.origin_id)
        self.message_bus.send_msg(propogate_loc) 
        

    def localize(self, new_loc_msg): 
        '''If the device has a higher id than the message coming in then it must not be the origin'''
        if self.origin_id < new_loc_msg.origin_id:
            '''Would you need to send a new message here?'''
            return        
        else:
            if self.assignment_dist == 0 or (self.assignment_dist > new_loc_msg.hops):
                if new_loc_msg.source == messages.Source.NORTH:
                    self.locale = tuple(new_loc_msg.location[0], new_loc_msg.location[0]  - 1)
                elif new_loc_msg.source == messages.Source.SOUTH:
                    self.locale = tuple(new_loc_msg.location[0], new_loc_msg.location[0]  + 1)
                '''
                elif new_loc_msg.source == messages.Source.EAST:
                    self.locale = tuple(new_loc_msg.location[0] - 1, new_loc_msg.location[0])
                elif new_loc_msg.source == messages.Source.WEST:
                    self.locale = tuple(new_loc_msg.location[0] + 1, new_loc_msg.location[0])
                '''
                self.origin_id = new_loc_msg.origin_id
                self.assignment_dist = new_loc_msg.hops

                if new_loc_msg.hops < new_loc_msg.ttl:
                    propogate_loc = LocalizationMessage(self.ID, self.locale, new_loc_msg.ttl, new_loc_msg.hops + 1, self.origin_id)
                    self.message_bus.send_msg(propogate_loc) 

        
