import zmq
import argparse
import multiprocessing as mp

parser = argparse.ArgumentParser(description='Simulates the Programmable Interrupt Controller')
parser.add_argument('device', type=str, help='PORT of Device')
parser.add_argument('north_RX', type=str, help='IN PORT of the North side connection')
parser.add_argument('west_RX',  type=str, help='IN PORT of the West side connection')
parser.add_argument('south_RX', type=str, help='IN PORT of the South side connection')
parser.add_argument('east_RX',  type=str, help='IN PORT of the East side connection')
parser.add_argument('north_TX', type=str, help='OUT PORT of the North side connection')
parser.add_argument('west_TX',  type=str, help='OUT PORT of the West side connection')
parser.add_argument('south_TX', type=str, help='OUT PORT of the South side connection')
parser.add_argument('east_TX',  type=str, help='OUT PORT of the East side connection')

URL = "tcp://127.0.0.1:"

class PICSim():
	def init(self, device, north_rx, south_rx, east_rx, west_rx, north_tx, south_tx, east_tx, west_tx):
		self.CONNECTIONS["DEVICE"] = device
		self.CONNECTIONS["NORTH_RX"] = north_rx
		self.CONNECTIONS["SOUTH_RX"] = south_rx
		self.CONNECTIONS["EAST_RX"] = east_rx
		self.CONNECTIONS["WEST_RX"] = west_rx

		self.CONNECTIONS["NORTH_TX"] = north_tx
		self.CONNECTIONS["SOUTH_TX"] = south_tx
		self.CONNECTIONS["EAST_TX"] = east_tx
		self.CONNECTIONS["WEST_TX"] = west_tx

		self.context = zmq.Context()

		self.start_server()
		self.bind_tx()

		self.inbox = []
		self.outbox = []

	def startup(self):
		self.connect_rx()

		self.TX_proc = mp.Process(target=self.TX)
		self.RX_proc = mp.Process(target=self.RX)
		self.send_proc = mp.Process(target=self.send)
		self.receive_proc = mp.Process(target=self.receive)

		self.TX_proc.start()
		self.RX_proc.start()
		self.send_proc.start()
		self.receive_proc.start()

		self.TX_proc.join()
		self.RX_proc.join()
		self.send_proc.join()
		self.receive_proc.join()

	def start_server(self):


		''' FIGURE THIS OUT '''

		self.device = self.context.socket(zmq.REP)
		self.device.bind(URL + self.CONNECTIONS["DEVICE"])
		return

	def bind_tx(self):
		self.north_tx = self.context.socket(zmq.PUSH)
		self.north_tx.bind(URL + self.CONNECTIONS["NORTH_TX"])

		self.south_tx = self.context.socket(zmq.PUSH)
		self.south_tx.bind(URL + self.CONNECTIONS["SOUTH_TX"])

		self.east_tx = self.context.socket(zmq.PUSH)
		self.east_tx.bind(URL + self.CONNECTIONS["EAST_TX"])

		self.west_tx = self.context.socket(zmq.PUSH)
		self.west_tx.bind(URL + self.CONNECTIONS["WEST_TX"])

		return

	def connect_rx(self):
		self.north_rx = self.context.socket(zmq.PULL)
		self.north_rx.connect(URL + self.CONNECTIONS["NORTH_RX"])

		self.south_rx = self.context.socket(zmq.PULL)
		self.south_rx.connect(URL + self.CONNECTIONS["SOUTH_RX"])

		self.east_rx = self.context.socket(zmq.PULL)
		self.east_rx.connect(URL + self.CONNECTIONS["EAST_RX"])

		self.west_rx = self.context.socket(zmq.PULL)
		self.west_rx.connect(URL + self.CONNECTIONS["WEST_RX"])

	def send_msg(self, dest, msg):
		'''Test RX/TX part'''
		self.outbox.append({dest, msg})
		return

	def recieve_msgs(self):
		'''Test RX/TX part'''
		msgs = self.inbox
		self.inbox = []
		return msgs

	def send(self):

		''' FIGURE THIS OUT '''

		while true:


	def receive(self):

		''' FIGURE THIS OUT '''

	def RX(self):
		while true:
			msg = self.north_rx.recv()
			if msg != None:
				self.inbox.append(msg)
			msg = self.south_rx.recv()
			if msg != None:
				self.inbox.append(msg)
			msg = self.east_rx.recv()
			if msg != None:
				self.inbox.append(msg)
			msg = self.west_rx.recv()
			if msg != None:
				self.inbox.append(msg)

	def TX(self):
		while true:
			if len(self.outbox) != 0:
				msg = self.outbox.pop
				if msg.dest == "NORTH":
					self.north_tx.send(msg.content)
				elif msg.dest == "SOUTH":
					self.south_tx.send(msg.content)
				elif msg.dest == "EAST":
					self.east_tx.send(msg.content)
				elif msg.dest == "WEST":
					self.west_tx.send(msg.content)
				else:
					exit(1)

def main():
	args = parser.parse_args()
	init_PIC(args["device"], args["north_RX"], args["south_RX"], args["east_RX"], args["west_RX"], args["north_TX"], args["south_TX"], args["east_TX"], args["west_TX"])

if __name__ == "__main__":
	main()
