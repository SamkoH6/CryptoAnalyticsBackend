from components.market_overview import *
import numpy as np

def calculate_volatility(prices):
    if prices.ndim == 2:
        returns = np.diff(prices[:, 1]).flatten() / prices[:-1, 1]
    elif prices.ndim == 1:
        returns = np.diff(prices).flatten() / prices[:-1]
    else:
        raise ValueError("Invalid shape for prices array")

    volatility = np.std(returns)
    return volatility