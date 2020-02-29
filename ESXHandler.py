import time
from Candle import Candle
#import matplotlib.pyplot as plt

TIMEFRAME = 30

#TYPE=PRICE|FEEDCODE=SP-FUTURE|BID_PRICE=2925.5|BID_VOLUME=916|ASK_PRICE=2925.75|ASK_VOLUME=1173

class ESXHandler:
	def __init__(self):
		self.start = time.time()
		self.bidPrices = []
		self.askPrices = []
		self.bidCandles = []
		self.askCandles = []
		self.midpoint = -1

	def handleMessage(self, data):
		splitData = data.split("|")
		if(data.startswith("TYPE=TRADE")):
			currentTrade = Trade(splitData[1].split("=")[1], splitData[2].split("=")[1], float(splitData[3].split("=")[1]), int(splitData[4].split("=")[1]))

		elif(data.startswith("TYPE=PRICE")):
			currentPrice = Price(splitData[1].split("=")[1], float(splitData[2].split("=")[1]),int(splitData[3].split("=")[1]),float(splitData[4].split("=")[1]),int(splitData[5].split("=")[1]))

	def getPrices(self, data):
		return float(data.split("|")[2].split("=")[1]),float(data.split("|")[4].split("=")[1])

	def handleData(self, data):
		if (time.time() - self.start < TIMEFRAME):
			if(data.startswith("TYPE=PRICE")):
				print("New Data")
				bidPrice, askPrice = self.getPrices(data)
				self.bidPrices.append(bidPrice)
				self.askPrices.append(askPrice)
		else:
			if len(self.bidPrices) > 0:
				self.bidCandles.append(Candle(self.bidPrices[0], self.bidPrices[-1], min(self.bidPrices), max(self.bidPrices)))

			if len(self.askPrices) > 0:
				self.askCandles.append(Candle(self.askPrices[0], self.askPrices[-1], min(self.askPrices), max(self.askPrices)))

			self.midpoint = sum(self.askPrices) / len(self.askPrices)

			#Setup for next Candle
			self.start = time.time()
			self.bidPrices.clear()
			self.askPrices.clear()
