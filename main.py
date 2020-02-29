from InformationRetriever import InformationRetriever
from Price import Price
from Trade import Trade
from Sender import Sender
import logging 
from ESXHandler import ESXHandler
from CandleDetector import CandleDetector

logging.basicConfig(filename='portfolio.log', filemode='w', format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

MIN_ESX_CANDLES = 1
BUY_AMOUNT = 50
SELL_AMOUNT = 50

PREV_BUY = -1
PREV_SELL = -1 


informationReceiver = InformationRetriever("35.179.45.135",7001)
sender = Sender()
ESXHandler = ESXHandler()

#TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=BID|PRICE=3350|VOLUME=3

#Read current data

count = 0
amount_esx = -3
amount_sp = 431
candleDetector = CandleDetector()

while count == 0:
	data = informationReceiver.receivePrices().decode("utf-8")
	logging.debug(data)
	print(data)
	if("SP-FUTURE" in data and "TYPE=PRICE" in data):
		
		ESXHandler.handleData(data)

		if(len(ESXHandler.askCandles) >= MIN_ESX_CANDLES):
			print("Midpoint: ",ESXHandler.midpoint, "Buy Price: ",ESXHandler.getPrices(data)[1]," Sell Price: ",ESXHandler.getPrices(data)[0])
			if(candleDetector.shouldBuy(ESXHandler.askCandles[-1]) or ESXHandler.getPrices(data)[1] < ESXHandler.midpoint):
				print("Buying at Price ",ESXHandler.getPrices(data)[1])
				PREV_BUY = sender.send_order("SP-FUTURE","BUY",ESXHandler.getPrices(data)[1], BUY_AMOUNT)
				print(PREV_BUY)

				if PREV_BUY != -1:
					amount_sp += BUY_AMOUNT
					logging.info("Buying price is:", PREV_BUY)
					logging.info("New count of SP-FUTURE Stock:", amount_sp)

			if((candleDetector.shouldSell(ESXHandler.bidCandles[-1]) or ESXHandler.getPrices(data)[0] > ESXHandler.midpoint) ):
				print("Selling at price", ESXHandler.getPrices(data)[0]); 
				PREV_SELL = sender.send_order("SP-FUTURE","SELL",ESXHandler.getPrices(data)[0], SELL_AMOUNT)
				print(PREV_SELL)
				logging.info(PREV_SELL)

				if PREV_SELL != -1:
					amount_sp -= SELL_AMOUNT
					logging.info("Selling price is:", PREV_BUY)
					logging.info("New count of SP-FUTURE Stock:", amount_sp)


			print(amount_sp)
