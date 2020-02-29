class Price:
	def __init__(self, feed, bidPrice, bidVolume, askPrice, askVolume):
		self.feed = feed
		self.bidPrice = bidPrice
		self.bidVolume = bidVolume
		self.askPrice = askPrice
		self.askVolume = askVolume

	def __str__(self):
		return self.feed+" BidPrice:"+self.bidPrice+" BidVolume:"+self.bidVolume+" AskPrice:"+self.askPrice+" AskVolume"+self.askVolume