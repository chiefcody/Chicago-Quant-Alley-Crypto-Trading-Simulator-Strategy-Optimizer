# Strategy.py
#This strategy executes a short straddle at 1 PM and exits based on price deviation or P&L thresholds.

from datetime import datetime
from utils.getStrikes import get_closest_strikes

class Strategy:
    def __init__(self, simulator):
        self.sim = simulator  # Reference to Simulator
        self.entryTime = None
        self.entryPrice = None
        self.callSymbol = None
        self.putSymbol = None
        self.positionOpen = False
        self.totalPnL = 0
        self.tradeLog = []

    def onMarketData(self, row):
        time = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
        symbol = row["Symbol"]

        # Entry: Detect 1 PM on day 1
        if time.hour == 13 and time.minute == 0 and not self.positionOpen:
            self.entryTime = time
            self.entryPrice = self.sim.currentPrice["MARK:BTCUSDT"]

            # Hardcoded ATM strikes (based on config)
            # self.callSymbol = "MARK:C-BTC-70000-20240601"
            # self.putSymbol = "MARK:P-BTC-70000-20240601"
            # Replace this:
            # self.callSymbol = "MARK:C-BTC-70000-20240601"
            # self.putSymbol = "MARK:P-BTC-70000-20240601"

            # Do this:
            all_symbols = self.sim.symbols
            atm_price = self.sim.currentPrice["MARK:BTCUSDT"]
            call_sym, put_sym = get_closest_strikes(atm_price, all_symbols)

            self.callSymbol = call_sym
            self.putSymbol = put_sym

            # Sell 0.1 qty of both call and put
            self.sim.onOrder(self.callSymbol, "SELL", 0.1, self.sim.currentPrice[self.callSymbol])
            self.sim.onOrder(self.putSymbol, "SELL", 0.1, self.sim.currentPrice[self.putSymbol])
            self.positionOpen = True
            print(f"Entered straddle at {self.entryTime}, underlying = {self.entryPrice}")

        # Exit logic
        if self.positionOpen:
            current_price = self.sim.currentPrice.get("MARK:BTCUSDT", 0)
            price_deviation = abs(current_price - self.entryPrice) / self.entryPrice
            if price_deviation > 0.01 or self.totalPnL >= 500 or self.totalPnL <= -500:
                # Exit: Buy back both options
                self.sim.onOrder(self.callSymbol, "BUY", 0.1, self.sim.currentPrice[self.callSymbol])
                self.sim.onOrder(self.putSymbol, "BUY", 0.1, self.sim.currentPrice[self.putSymbol])
                self.positionOpen = False
                print(f"Exited straddle at {time}, underlying = {current_price}, PnL = {round(self.totalPnL, 2)}")

    def onTradeConfirmation(self, symbol, side, quantity, price):
        value = quantity * price
        if side == "SELL":
            self.totalPnL += value
        elif side == "BUY":
            self.totalPnL -= value

        # Record the trade
        self.tradeLog.append({
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "side": side,
            "qty": quantity,
            "price": price,
            "pnl": round(self.totalPnL, 2)
        })

