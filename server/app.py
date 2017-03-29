from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
#from plugin_manager import PluginManager


class TwilightProtocol(LineReceiver):

    def __init__(self, units):
        self.units = units

    def getPeerTuple(self):
        peer = self.transport.getPeer()
        return (peer.host, peer.port)

    def connectionMade(self):
        peer_tuple = self.getPeerTuple()
        print('Client %s:%d connected' % peer_tuple)

    def connectionLost(self, reason):
        peer_tuple = self.getPeerTuple()
        if peer_tuple in self.units:
            del self.units[peer_tuple]
        print('Client %s:%d disconnected' % peer_tuple)

    def lineReceived(self, line):
        peer_tuple = self.getPeerTuple()
        command, _, line = line.decode('utf-8').strip().partition(' ')
        if command == 'INFO':
            line_parts = line.strip().split(' ')
            coordinates, teensy_id, hostname = line_parts[0], int(line_parts[1]), line_parts[2]
            ns, _, we = coordinates.partition(',')
            ns, we = int(ns), int(we)
            unit_dict = {
                'unit': hostname,
                'position_ns': ns,
                'position_we': we,
                'teensy_id': teensy_id
            }
            self.units[peer_tuple] = unit_dict
            print('Client %s:%d registered: %s - %d (%d, %d)' % (*peer_tuple, hostname, teensy_id, ns, we))
            print(self.units)

class TwilightFactory(Factory):

    def __init__(self):
        self.units = {}

    def buildProtocol(self, addr):
        return TwilightProtocol(self.units)

def main():
    reactor.listenTCP(8123, TwilightFactory())
    reactor.run()

if __name__ == "__main__":
    main()
