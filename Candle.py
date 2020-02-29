class Candle:
	def __init__(self, open, close, lowest, highest):
		self.open = open
		self.close = close
		self.lowest = lowest
		self.highest = highest

	def __str__(self):
		return self.open+" "+self.close+" "+self.lowest+" "+self.highest