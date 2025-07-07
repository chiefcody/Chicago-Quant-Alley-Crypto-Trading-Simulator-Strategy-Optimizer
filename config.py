#config.py


simStartDate = "20240601" #it tells the simulator to start reading data from that date in the format YYYYMMDD
simEndDate = "20240601"  #End date in the format YYYYMMDD for the backtest

symbols = [
    "MARK:BTCUSDT",
#This represents the market price of Bitcoin in USDT($)
#the strategy that i am using includes to read the price at 1pm .Then select the strike price and then observe the price movements during the day. If the price moves more than +/- 1%, we exit the trade.
    "MARK:C-BTC-69000-20240601",
    "MARK:P-BTC-69000-20240601",
    "MARK:C-BTC-70000-20240601",
#This is the call option on the BTC.Here the buyer's make profit if BTC goes above the strike price.
#In this strategy you sell 0.1 lots of this call option at 1pm, this earn u premium as the seller. U want the price to stay around 70,000 and not move far up.
    "MARK:P-BTC-70000-20240601",
#This is the put option on the BTC.Here the buyer's make profit if BTC goes below the strike price.
#In this strategy you sell 0.1 lots of this call option at 1pm, this earn u premium as the seller. U want the price to stay around 70,000 and not move far below.
    "MARK:C-BTC-71000-20240601",
    "MARK:P-BTC-71000-20240601"
]

#Straddle strategy is the strategy in which you profit only if the BTC price stays close to the strike price that is it has low volatility.
