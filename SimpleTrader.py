from InformationRetriever import InformationRetriever
from Sender import Sender
from sklearn import linear_model
from sklearn import metrics
from sklearn import ensemble
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


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

pod = 15
# clf = linear_model.LinearRegression()
clf = ensemble.GradientBoostingRegressor(n_estimators = 500, max_depth = 10, min_samples_split = 2,
	learning_rate = 0.2, loss = 'ls')
old_hist_SP_Ask = []
old_hist_SP_Bid = []
trade_hist_SP_Ask = []
trade_hist_SP_Bid = []

old_hist_ESX_Ask = []
old_hist_ESX_Bid = []
trade_hist_ESX_Ask = []
trade_hist_ESX_Bid = []

pred_ask_ESX = -1
pred_bid_ESX = -1
pred_ask_SP = -1
pred_bid_SP = -1

def gradientBoosting(pair, old_list, trade_list, biddi): 
	if len(old_list) < pod+1 or len(trade_list) < pod: 
		trade_list.append(pair)
		return -1 

	X = [[old_list[i-1], trade_list[i][0], trade_list[i][1]] for i in range(-1*pod, 0)]
	ask_X_train = np.array(X).astype(np.float64)
	Y = old_list[len(old_list) - pod:]
	ask_Y_train = np.array(Y).astype(np.float64)

	clf.fit(ask_X_train, ask_Y_train)
	trade_list.append(pair)
	y_pred = clf.predict([[old_list[-1], pair[0], pair[1]]])

	if biddi: 
		print("PREDICT BID   ", y_pred)
		return y_pred
	
	else: 
		print("PREDICT ASK   ", y_pred)
		return y_pred

THRESHHOLD = 0.1
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
	print(data)
	if("TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=BID" in data):
		instrument = 'ESX-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_bid_ESX = gradientBoosting([price, volume], old_hist_ESX_Bid, trade_hist_ESX_Bid, True)
 
 	if("TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=ASK" in data):
		instrument = 'ESX-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_ask_ESX = gradientBoosting([price, volume], old_hist_ESX_Ask, trade_hist_ESX_Ask, False)

	if("TYPE=TRADE|FEEDCODE=SP-FUTURE|SIDE=BID" in data):
		instrument = 'SP-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_bid_SP = gradientBoosting([price, volume], old_hist_SP_Bid, trade_hist_SP_Bid, True)
 
 	if("TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=ASK" in data):
		instrument = 'SP-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_ask_SP = gradientBoosting([price, volume], old_hist_SP_Ask, trade_hist_SP_Ask, False)

	if("TYPE=PRICE|FEEDCODE=SP-FUTURE" in data):
		instrument = 'SP-FUTURE'
		bidPrice, askPrice = getPrices(data)
		old_hist_SP_Bid.append(bidPrice)
		old_hist_SP_Ask.append(askPrice)

		# pred_ask, pred_bid = gradientBoosting(askPrice, bidPrice, old_hist_SP_Ask, old_hist_SP_Bid)

		# if (pred_ask > 0 and pred_ask - THRESHHOLD > askPrice):
		# 	#Buy
		# 	print("Buying 15 SP at ",askPrice)
		# 	fpLastBought = askPrice
		# 	sender.send_order(instrument,"BUY",askPrice,15)
		# 	continue

		# if (pred_bid > 0 and pred_bid + THRESHHOLD < bidPrice):
		# 	#print(bidPrice,(a+(len(bidPrices)+1)*b))
		# 	#Sell
		# 	print("Selling 15 SP at ",bidPrice)
		# 	sender.send_order(instrument,"SELL",bidPrice,15)


	if("TYPE=PRICE|FEEDCODE=ESX-FUTURE" in data):
		instrument = 'ESX-FUTURE'
		bidPrice, askPrice = getPrices(data)
		old_hist_ESX_Bid.append(bidPrice)
		old_hist_ESX_Ask.append(askPrice)
		# pred_ask, pred_bid = gradientBoosting(askPrice, bidPrice, old_hist_ESX_Ask, old_hist_ESX_Bid)

		# if (pred_ask > 0 and pred_ask - THRESHHOLD > askPrice):
		# 	#Buy
		# 	print("Buying 15 ESX at ",askPrice)
		# 	fpLastBought = askPrice
		# 	sender.send_order(instrument,"BUY",askPrice,15)
		# 	continue

		# if (pred_bid > 0 and pred_bid + THRESHHOLD < bidPrice):
		# 	#print(bidPrice,(a+(len(bidPrices)+1)*b))
		# 	#Sell
		# 	print("Selling 15 ESX at ",bidPrice)
		# 	sender.send_order(instrument,"SELL",bidPrice,15)






