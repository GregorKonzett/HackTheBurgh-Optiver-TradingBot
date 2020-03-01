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

def handleMessage(self, data):
	splitData = data.split("|")
	if(data.startswith("TYPE=TRADE")):
		currentTrade = Trade(splitData[1].split("=")[1], splitData[2].split("=")[1], float(splitData[3].split("=")[1]), int(splitData[4].split("=")[1]))

	elif(data.startswith("TYPE=PRICE")):
		currentPrice = Price(splitData[1].split("=")[1], float(splitData[2].split("=")[1]),int(splitData[3].split("=")[1]),float(splitData[4].split("=")[1]),int(splitData[5].split("=")[1]))



while count == 0:
	data = informationReceiver.receivePrices().decode("utf-8")
	logging.debug(data)
	print(data)
	