class Trade:
	def __init__(self,feed, side,price,volume):
		self.feed = feed
		self.side = side
		self.price = price
		self.volume = volume


	def __str__(self):
		return self.feed+" "+self.side+" "+self.price+" "+self.volume