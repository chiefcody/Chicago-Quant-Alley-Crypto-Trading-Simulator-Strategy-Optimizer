# Quant Strategy Simulator

This is a modular, event-driven trading simulator for testing simple options strategies like straddles.

## Structure

- `Simulator.py`: Main simulation logic
- `Strategy.py`: Strategy logic
- `config.py`: Settings like start date, symbols
- `data/`: CSV data for each symbol
- `utils/getStrikes.py`:Dynamically finds closest strike options
- `stats/printStats.py`: Analysis and plotting
- `output/` – PnL logs and plot images
  
