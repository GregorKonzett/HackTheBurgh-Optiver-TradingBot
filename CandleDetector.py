RANGE = 0.80

class CandleDetector:
	def shouldBuy(self, candle):
		return (candle.close >= (RANGE * (candle.highest))) and candle.close > candle.open > candle.lowest

	def shouldSell(self, candle):
		return candle.open >= RANGE * candle.highest and candle.open  < candle.highest * (2 - RANGE) and candle.lowest < candle.close
