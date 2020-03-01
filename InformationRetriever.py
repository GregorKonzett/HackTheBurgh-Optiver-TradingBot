import socket

class InformationRetriever:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.sendto("TYPE=SUBSCRIPTION_REQUEST".encode(),(self.ip,self.port))


	def receivePrices(self):
		data, addr = self.sock.recvfrom(1024)
		return data
		