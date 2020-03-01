from InformationRetriever import InformationRetriever
from Sender import Sender
from sklearn import linear_model
from sklearn import metrics
from sklearn import ensemble
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


X = []
SPY = []

def getPrices(data):
	return float(data.split("|")[2].split("=")[1]),float(data.split("|")[4].split("=")[1])

def bestLine(prices):
	sumX = (len(prices)*(len(prices)+1))/2
	xAverage = sumX/len(prices)

	sumY = sum(prices)
	yAverage = sumX / len(prices)

	sumXSquared = 0
	sumMul = 0

	for i in range(len(prices)):
		sumMul += ((i+1)-xAverage)*(prices[i]-yAverage)
		sumXSquared += ((i+1)-xAverage)*((i+1)-xAverage)

	b = sumMul/sumXSquared
	a = (sumY - b*sumX)/len(prices)

	return a,b

def parse(item): 
#TYPE=PRICE|FEEDCODE=SP-FUTURE|BID_PRICE=3011|BID_VOLUME=1853|ASK_PRICE=3011.25|ASK_VOLUME=257
	return float(data.split("|")[2].split("=")[1]), float(data.split("|")[3].split("=")[1]), float(data.split("|")[4].split("=")[1]), float(data.split("|")[5].split("=")[1])

def gradientBoosting(item): 
	bidP, bidVol, askP, askVol = parse(item)
	if len(SPY) >= 10: 
		x_train = np.array(X).astype(np.float64)
		clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
				learning_rate = 0.1, loss = 'ls')
		clf.fit(x_train, np.array(SPY).astype(np.float))
		x_test = np.array([bidP, bidVol, askP, askVol]).astype(np.float64).reshape(1,-1)
		y_pred = clf.predict(x_test)
		print("\n\tPREDICT SPY", y_pred)

	X.append([bidP, bidVol, askP, askVol])

PRICES_LENGTH = 15
THRESHHOLD = 0.5
AMOUNT_SCALING = 10

informationRetriever = InformationRetriever("35.179.45.135",7001)
sender = Sender()

bidPrices = []
askPrices = []

esxBidPrices = []
esxAskPrices = []

fpLastBought = -1
esxLastBought = -1

while True:
	data = informationRetriever.receivePrices().decode("utf-8")
	if("TYPE=PRICE|FEEDCODE=SP-FUTURE" in data):
		print(data)
		bidPrice, askPrice = getPrices(data)

		if (len(X) > 0):
			SPY.append(askPrice)
			print("Actual SPY ASK PRICE IS: ", askPrice)

		if(len(askPrices) >= PRICES_LENGTH):
			a,b = bestLine(askPrices)

			if (askPrice + THRESHHOLD < a+(len(askPrices)+1)*b):
				#Buy
				print("Buying FP at ",askPrice)
				fpLastBought = askPrice
				sender.send_order("SP-FUTURE","BUY",askPrice,10)
				continue

		if(len(bidPrices) >= PRICES_LENGTH):
			a,b = bestLine(bidPrices)
			
			if (bidPrice + THRESHHOLD < a+(len(bidPrices)+1)*b):
				print(bidPrice,(a+(len(bidPrices)+1)*b))
				#Sell
				print("Selling FP at ",bidPrice)
				sender.send_order("SP-FUTURE","SELL",bidPrice,15)

		if(len(bidPrices) >= PRICES_LENGTH):
			del(bidPrices[0])
		
		bidPrices.append(bidPrice)

		if(len(askPrices) >= PRICES_LENGTH):
			del(askPrices[0])

		askPrices.append(askPrice)

	if("TYPE=PRICE|FEEDCODE=ESX-FUTURE" in data):
		print(data)
		esxBidPrice, esxAskPrice = getPrices(data)

		gradientBoosting(data)

		if(len(esxAskPrices) >= PRICES_LENGTH):
			a,b = bestLine(esxAskPrices)

			if (esxAskPrice + THRESHHOLD < a+(len(esxAskPrices)+1)*b):
				#Buy
				print("Buying ESX at ",esxAskPrice)
				esxLastBought = esxAskPrice
				sender.send_order("SP-FUTURE","BUY",esxAskPrice,10)
				continue

		if(len(esxBidPrices) >= PRICES_LENGTH):
			a,b = bestLine(esxBidPrices)

			if (esxBidPrice + THRESHHOLD < a+(len(esxBidPrices)+1)*b and esxBidPrice > esxLastBought):
				#Sell
				print("Selling ESX at ",esxBidPrice)
				sender.send_order("SP-FUTURE","SELL",esxBidPrice,15)

		if(len(esxBidPrices) >= PRICES_LENGTH):
			del(esxBidPrices[0])
		
		esxBidPrices.append(esxBidPrice)

		if(len(esxAskPrices) >= PRICES_LENGTH):
			del(esxAskPrices[0])

		esxAskPrices.append(esxAskPrice)





