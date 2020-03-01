from InformationRetriever import InformationRetriever
from Sender import Sender
# from sklearn import linear_model
from sklearn import ensemble
import numpy as np


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


pod = 10
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

esx_last_bought = -1
sp_last_bought = -1

esx_last_bid = -1
sp_last_bid = -1

esx_bidPrice = 0
esx_askPrice = 0

sp_bidPrice = 0
sp_askPrice = 0

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


THRESHHOLD = 0.24
AMOUNT = 0.3
informationRetriever = InformationRetriever("35.179.45.135",7001)
sender = Sender()


while True:
	data = informationRetriever.receivePrices().decode("utf-8")
	print(data)
	if("TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=BID" in data):
		instrument = 'ESX-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_bid_ESX = gradientBoosting([price, volume], old_hist_ESX_Bid, trade_hist_ESX_Bid, True)
		esx_last_bid = esx_bidPrice

		if (pred_bid_ESX > 0 and pred_bid_ESX + THRESHHOLD < esx_bidPrice and esx_bidPrice > esx_last_bought):
			#Sell
			print("Selling 50 ESX at ",esx_bidPrice)
			sender.send_order(instrument,"SELL",esx_bidPrice,round(volume*AMOUNT))

	elif("TYPE=TRADE|FEEDCODE=ESX-FUTURE|SIDE=ASK" in data):
		instrument = 'ESX-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_ask_ESX = gradientBoosting([price, volume], old_hist_ESX_Ask, trade_hist_ESX_Ask, False)
		if (pred_ask_ESX > 0 and pred_ask_ESX - THRESHHOLD >= esx_askPrice and esx_askPrice < esx_last_bid):
			#Buy
			esx_last_bought = esx_askPrice
			print("Buying 50 ESX at ",esx_askPrice)
			sender.send_order(instrument,"BUY",esx_askPrice,round(volume*AMOUNT))


	elif("TYPE=TRADE|FEEDCODE=SP-FUTURE|SIDE=BID" in data):
		instrument = 'SP-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_bid_SP = gradientBoosting([price, volume], old_hist_SP_Bid, trade_hist_SP_Bid, True)

		sp_last_bid = sp_bidPrice
		if (pred_bid_SP > 0 and pred_bid_SP + THRESHHOLD < sp_bidPrice and sp_bidPrice > sp_last_bought):
			#print(bidPrice,(a+(len(bidPrices)+1)*b))
			#Sell
			print("Selling 50 SP at ",sp_bidPrice)
			sender.send_order(instrument,"SELL",sp_bidPrice,round(volume*AMOUNT))

 
	elif("TYPE=TRADE|FEEDCODE=SP-FUTURE|SIDE=ASK" in data):
		instrument = 'SP-FUTURE'
		price, volume = float(data.split("|")[3].split("=")[1]),float(data.split("|")[4].split("=")[1])
		pred_ask_SP = gradientBoosting([price, volume], old_hist_SP_Ask, trade_hist_SP_Ask, False)

		if (pred_ask_SP > 0 and pred_ask_SP - THRESHHOLD > sp_askPrice and sp_askPrice < sp_last_bid):
			#Buy
			sp_last_bought = sp_askPrice
			print("Buying 50 SP at ",sp_askPrice)
			sender.send_order(instrument,"BUY",sp_askPrice,round(volume*AMOUNT))


	elif("TYPE=PRICE|FEEDCODE=SP-FUTURE" in data):
		instrument = 'SP-FUTURE'
		sp_bidPrice, sp_askPrice = getPrices(data)
		old_hist_SP_Bid.append(sp_bidPrice)
		old_hist_SP_Ask.append(sp_askPrice)


	elif("TYPE=PRICE|FEEDCODE=ESX-FUTURE" in data):
		instrument = 'ESX-FUTURE'
		esx_bidPrice, esx_askPrice = getPrices(data)
		old_hist_ESX_Bid.append(esx_bidPrice)
		old_hist_ESX_Ask.append(esx_askPrice)





