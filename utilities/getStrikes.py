# utils/getStrikes.py

import re

def extract_strike(symbol):
    """
    Extracts the strike price from a symbol string like:
    "MARK:C-BTC-70000-20240601"
    Returns: 70000.0
    """
    match = re.search(r"-BTC-(\d+)-", symbol)
    if match:
        return float(match.group(1))
    return None

def get_closest_strikes(futures_price, symbols, option_type="both", tolerance=0.02):
    """
    Returns the closest call and put option symbols near the given futures price.

    Parameters:
    - futures_price: the current ATM price of BTC
    - symbols: list of all available option symbols (strings)
    - option_type: "call", "put", or "both"
    - tolerance: max % distance allowed (e.g., 0.02 = ±2%)

    Returns:
    - (closest_call_symbol, closest_put_symbol)
    """
    closest_call = None
    closest_put = None
    min_call_diff = float('inf')
    min_put_diff = float('inf')

    for symbol in symbols:
        if ":C-BTC-" in symbol:
            strike = extract_strike(symbol)
            if strike and abs(strike - futures_price) / futures_price <= tolerance:
                diff = abs(strike - futures_price)
                if diff < min_call_diff:
                    closest_call = symbol
                    min_call_diff = diff

        elif ":P-BTC-" in symbol:
            strike = extract_strike(symbol)
            if strike and abs(strike - futures_price) / futures_price <= tolerance:
                diff = abs(strike - futures_price)
                if diff < min_put_diff:
                    closest_put = symbol
                    min_put_diff = diff

    return closest_call, closest_put
