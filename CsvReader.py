import pandas as pd 
import matplotlib.pyplot as plt

market = pd.read_csv("market_data.csv")
trades = pd.read_csv("trades.csv")

#print(market.head()) 
 # Timestamp  Instrument  Bid Price  Bid Volume  Ask Price  Ask Volume
#market.plot(kind='scatter',x='Timestamp',y='Bid Price',color='red')
plt.show()
