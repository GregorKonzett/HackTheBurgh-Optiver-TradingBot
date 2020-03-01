import logging 
import csv 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
#from sklearn.neighbors import KNeighborsRegressor


LONG_AVERAGE_NUMBER = 200
SHORT_AVERAGE_NUMBER = 50
THRESHOLD = 5
AMOUNT = 1

#Ask price always 0.25 > than big price

class MovingAvg:
	def __init__(self):
		self.longAvgs = []
		self.shortAvgs = []
		self.longAvg = -1
		self.shortAvg = -1
		self.ready = False
		self.count = 0
		self.money = 20000
	
	def regression(): 
		KNeighborsRegressor(algorithm='brute')
		market = pd.read_csv('market_data.csv')
		trade = pd.read_csv('trades.csv')


	def updateAverages(self, price):
		#Update Long Average
		if(len(self.longAvgs) >= LONG_AVERAGE_NUMBER):
			self.ready = True
			del(self.longAvgs[0])
		
		self.longAvgs.append(price)
		self.longAvg = (len(self.longAvgs) - sum(self.longAvgs)) / len(self.longAvgs)

		#Update Short Average
		if(len(self.shortAvgs) >= SHORT_AVERAGE_NUMBER):
			del(self.shortAvgs[0])
		
		self.shortAvgs.append(price)
		self.shortAvg = (len(self.shortAvgs)-sum(self.shortAvgs)) / len(self.shortAvgs)

	def compareAverages(self, price):
		diff = self.shortAvg - self.longAvg
		
		if (diff > THRESHOLD): #Buy
			print("Long: ",self.longAvg," Short: ",self.shortAvg," Diff: ",diff)
			amt = self.money // (price+0.25)
			self.count += amt
			self.money -= amt * (price+0.25)
			print("BUY at", price, "AMOUNT LEFT : ", self.count, " MONEY: ",self.money)
		elif (diff < THRESHOLD*-1 and self.count >= AMOUNT): #Sell
			self.count -= AMOUNT
			self.money += AMOUNT * price
			print("SELL at", price, " AMOUNT LEFT: ", self.count, " MONEY: ",self.money)

	def main(self):
		#market = csv.DictReader(open("market_data.csv", 'r'))
		# trade = csv.DictReader(open("trades.csv", 'r')) 
		count = 0 
		
		#Plot Market
		market = pd.read_csv('market_data.csv')
		trade = pd.read_csv('trades.csv')
		# esx = market[market["Instrument"] == "ESX-FUTURE"]
		# sp = market[market["Instrument"] == "SP-FUTURE"]
		#fig = px.line(market[market["Instrument"] == "ESX-FUTURE"],x = "Timestamp",y="Bid Price")
		# fig.add_scatter(sp, x = "Timestamp", y="Bid Price")
		#fig.show()

		# fig1 = px.add_trace(trade[trade["Traded Instrument"] == "ESX-FUTURE"],x = "Timestamp",y="Traded Price",mode='markers',color="Traded Side")
		# fig1.show()
		#fig1 = px.line(market[market["Instrument"] == "SP-FUTURE"],x="Timestamp",y="Bid Price")
		#fig1.show()

		#for row in market.iterrows():
		#	row["Timestamp"] = self.get_sec(market['Timestamp']) - self.get_sec("11:43:08")
		fig = go.Figure()

		

		subset = trade[trade["Traded Instrument"] == "SP-FUTURE"]
		spMarket = market[market["Instrument"] == "SP-FUTURE"]
		buys = subset[subset["Traded Side"] == "ASK"]
		sells = subset[subset["Traded Side"] == "BID"]

		count = 0
		for i,row in spMarket.iterrows():
			spMarket.set_value(i,"Timestamp",count)
			count += 1

		count = 0
		for i,row in buys.iterrows():
			buys.set_value(i,"Timestamp",count)
			count += 1
			
		count = 0	
		for i,row in sells.iterrows():
			sells.set_value(i,"Timestamp",count)
			count += 1
	
	
		#spMarket.plot.scatter(x="Timestamp",y="Bid Price")

		plt.plot(spMarket["Timestamp"],spMarket["Bid Price"])
		plt.plot(buys["Timestamp"], buys["Traded Price"])
		#plt.scatter(buys["Timestamp"],buys["Traded Price"],c="b")
		#plt.scatter(sells["Timestamp"],sells["Traded Price"],c="g")
		plt.show()
		#market['Timestamp'] = self.get_sec(market['Timestamp']) - self.get_sec(market.loc[0]['Timestamp'])
		

		return 
		
		fig1 = go.Figure()
		fig1.add_trace(go.Scatter(x=pd.read_csv('market_data.csv')["Timestamp"],y=market[market["Instrument"] == "SP-FUTURE"]["Bid Price"],mode="lines",name="Market"))
		
		#fig1.add_trace(go.Scatter(x=buys["Timestamp"],y=buys["Traded Price"],mode="lines",name="Buys"))
		#fig1.add_trace(go.Scatter(x=sells["Timestamp"],y=sells["Traded Price"],mode="lines",name="Sells"))
		#fig1.show()
		return
		for i,row in market.iterrows():
			market.set_value(i,"Timestamp",i)

		for i,row in buys.iterrows():
			buys.set_value(i,"Timestamp",i/2)
			
		for i,row in sells.iterrows():
			sells.set_value(i,"Timestamp",i/2)

		fig.add_trace(go.Scatter(x=market["Timestamp"],y=market[market["Instrument"] == "SP-FUTURE"]["Bid Price"],mode="lines",name="Market"))
		fig.add_trace(go.Scatter(x=buys["Timestamp"],y=buys["Traded Price"],mode="lines",name="Buys"))
		fig.add_trace(go.Scatter(x=sells["Timestamp"],y=sells["Traded Price"],mode="lines",name="Sells"))
		fig.show()
		#fig.add_trace(go.Scatter(x=random_x, y=random_y0,
        #            mode='markers',
        #            name='markers'))
		#12:29:28 for trade
		#13:33:1521


		#12:46:14 + 01:03:47 (3827s)




MovingAvg().main()
				