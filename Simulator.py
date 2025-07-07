# Simulator.py
# We are creating a modular trading simulator that loads historical price data, feeds it to a trading strategy, simulates trades and then tracks and prints final profit and loss (PnL) 

import os
import pandas as pd
from datetime import datetime, timedelta
from Strategy import Strategy
import config


class Simulator:
    def __init__(self):
        # Load configuration from config.py, converts the start and end dates into proper date objects ,stores the list of symbols ill trade.
        self.startDate = datetime.strptime(config.simStartDate, "%Y%m%d")
        self.endDate = datetime.strptime(config.simEndDate, "%Y%m%d")
        self.symbols = config.symbols

        # Initialize variables
        self.df = pd.DataFrame()
        self.currentPrice = {}
        self.currQuantity = {}
        self.buyValue = {}
        self.sellValue = {}
        self.slippage = 0.0001  # 0.01% slippage
#Slippage is the small difference between the expected price of a trade and the actual price you get when the trade is executed.

        for sym in self.symbols:
            self.currentPrice[sym] = 0.0
            self.currQuantity[sym] = 0.0
            self.buyValue[sym] = 0.0
            self.sellValue[sym] = 0.0

        # Initialize the strategy
        self.strategy = Strategy(self)

        # Load data and start simulation
        self.readData()
        self.startSimulation()

    def readData(self):
        """Load and merge data from all dates and symbols"""
        data_frames = []
        curr_date = self.startDate

        while curr_date <= self.endDate:
            folder = os.path.join("data", curr_date.strftime("%Y%m%d"))
            for symbol in self.symbols:
                filename = os.path.join(folder, f"{symbol}.csv")
                if os.path.exists(filename):
                    df = pd.read_csv(filename)
                    df["Symbol"] = symbol
                    data_frames.append(df)
            curr_date += timedelta(days=1)

#merge them into one big table and sort the rows by timestamp
        if data_frames:
            self.df = pd.concat(data_frames)
            self.df = self.df.sort_values(by="timestamp").reset_index(drop=True)
        else:
            print("No data files found.")

    def startSimulation(self):
        """Main event loop that feeds data to the strategy"""
        for _, row in self.df.iterrows():
            symbol = row["Symbol"]
            price = row["price"]
            self.currentPrice[symbol] = price
            self.strategy.onMarketData(row)

    def onOrder(self, symbol, side, quantity, price):
        """Simulate trade execution with slippage"""
        if symbol not in self.currentPrice:
            print(f"Warning: No current price for {symbol}")
            return

        if side == "BUY":
            trade_price = price * (1 + self.slippage)
            self.currQuantity[symbol] += quantity
            self.buyValue[symbol] += trade_price * quantity
        elif side == "SELL":
            trade_price = price * (1 - self.slippage)
            self.currQuantity[symbol] -= quantity
            self.sellValue[symbol] += trade_price * quantity
        else:
            print(f"Invalid side: {side}")
            return

        self.strategy.onTradeConfirmation(symbol, side, quantity, trade_price)

    def printPnl(self):
        """Calculate total PnL (realized + unrealized)"""
        total_pnl = 0.0
        for sym in self.symbols:
            price = self.currentPrice.get(sym, 0)
            quantity = self.currQuantity.get(sym, 0)
            realized = self.sellValue[sym] - self.buyValue[sym]
            unrealized = quantity * price
            total_pnl += realized + unrealized
        print(f"Total P&L: {round(total_pnl, 2)}")


# Run the simulator
if __name__ == "__main__":
    sim = Simulator()
    sim.printPnl()

#Save trade log to CSV for analysis
import os
os.makedirs("output", exist_ok=True)

import pandas as pd
pd.DataFrame(sim.strategy.tradeLog).to_csv("output/trade_log.csv", index=False)
print("Trade log saved to output/trade_log.csv")
