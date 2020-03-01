import socket
import logging

USERNAME = 'Team30'
PASSWORD = 'LqF7DuPT'

REMOTE_IP = "35.179.45.135"
EML_UDP_PORT_REMOTE = 8001
EML_UDP_PORT_LOCAL = 8078
UDP_ANY_IP = ""

class Sender:
	def __init__(self):
		self.eml_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.eml_sock.bind((UDP_ANY_IP, EML_UDP_PORT_LOCAL))


	def send_order(self, target_feedcode, action, target_price, volume):
		"""
		Send an order to the exchange.
		:param target_feedcode: The feedcode, either "SP-FUTURE" or "ESX-FUTURE"
		:param action: "BUY" or "SELL"
		:param target_price: Price you want to trade at
		:param volume: Volume you want to trade at. Please start with 10 and go from there. Don't go crazy!
		:return:
		Example:
		If you want to buy  100 SP-FUTURES at a price of 3000:
		- send_order("SP-FUTURE", "BUY", 3000, 100)
		"""

		if volume == 0:
			return -1

		order_message = "TYPE=ORDER|USERNAME={}|PASSWORD={}|FEEDCODE={}|ACTION={}|PRICE={}|VOLUME={}".format(USERNAME,PASSWORD,target_feedcode,action,target_price,volume)
		print("[SENDING ORDER] {}".format(order_message))
		self.eml_sock.sendto(order_message.encode(), (REMOTE_IP, EML_UDP_PORT_REMOTE))

		data, addr = self.eml_sock.recvfrom(1024)
		message = (data.decode("utf-8"))
		print(message)
		if message[-2:] != '=0':
			return target_price
		else:
			return -1
	
#sender.send_order("ESX-FUTURE","SELL",3400,1)