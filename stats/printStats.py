# printStats.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the trade log from a CSV (generated after simulation)
df = pd.read_csv("output/trade_log.csv")

# Keep only one row per timestamp to avoid double-counting
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Create a time series of cumulative PnL
df["cum_pnl"] = df["pnl"]
df.set_index("timestamp", inplace=True)

# Fill missing minutes if needed
# df = df.asfreq("T", method="ffill")

# Calculate returns
df["returns"] = df["cum_pnl"].diff().fillna(0)

# === Metrics === #
mean_pnl = df["cum_pnl"].mean()
median_pnl = df["cum_pnl"].median()
std_pnl = df["cum_pnl"].std()

daily_return = df["returns"].sum()
sharpe = (df["returns"].mean() / df["returns"].std()) * np.sqrt(1440)  # 1440 mins/day

# Max drawdown
cum_max = df["cum_pnl"].cummax()
drawdown = df["cum_pnl"] - cum_max
max_dd = drawdown.min()

# VaR & Expected Shortfall at 95%
VaR_95 = np.percentile(df["returns"], 5)
ES_95 = df["returns"][df["returns"] < VaR_95].mean()

# === Output === #
print("Performance Metrics:")
print(f"Mean PnL: ₹{mean_pnl:.2f}")
print(f"Median PnL: ₹{median_pnl:.2f}")
print(f"Std Dev: ₹{std_pnl:.2f}")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Max Drawdown: ₹{max_dd:.2f}")
print(f"VaR 95%: ₹{VaR_95:.2f}")
print(f"Expected Shortfall (95%): ₹{ES_95:.2f}")

# === Plots === #
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["cum_pnl"], label="Cumulative PnL", color="green")
plt.title("Cumulative PnL")
plt.xlabel("Time")
plt.ylabel("PnL")
plt.grid()
plt.legend()
plt.savefig("output/pnl_plot.png")

plt.figure(figsize=(12, 6))
plt.plot(df.index, drawdown, label="Drawdown", color="red")
plt.title("Drawdown Curve")
plt.xlabel("Time")
plt.ylabel("Drawdown")
plt.grid()
plt.legend()
plt.savefig("output/drawdown_plot.png")

print("\nPlots saved to output/ folder.")

