from components.market_overview import *
import numpy as np
import pandas as pd

def calculate_daily_returns(prices):
    if prices.ndim == 1:
        # If prices is one-dimensional
        return np.diff(prices) / prices[:-1]
    elif prices.ndim == 2:
        # If prices is two-dimensional, assume the price data is in the second column
        return np.diff(prices[:, 1]) / prices[:-1, 1]
    else:
        raise ValueError("Invalid shape for prices array")
    
def perform_correlation_analysis(api_key, crypto_symbol, stock_symbol, days=30):
    # Get historical prices for cryptocurrency
    history_data_crypto = get_historical_prices(api_key, crypto_symbol, days)
    crypto_prices = np.array(history_data_crypto.get('prices', [])).astype(float)
    
    # Get historical prices for the stock index
    history_data_stock = get_historical_prices(api_key, stock_symbol, days)
    stock_prices = np.array(history_data_stock.get('prices', [])).astype(float)

    # Calculate daily returns
    crypto_returns = calculate_daily_returns(crypto_prices)
    stock_returns = calculate_daily_returns(stock_prices)

    # Check for NaN values
    if np.isnan(crypto_returns).any() or np.isnan(stock_returns).any():
        print("Warning: NaN values detected in daily returns. Data cleaning may be required.")
    
    # Create a DataFrame for easier analysis
    data = pd.DataFrame({f'{crypto_symbol} Returns': crypto_returns, f'{stock_symbol} Returns': stock_returns})

    # Check for NaN values in the DataFrame
    if data.isnull().values.any():
        print("Warning: NaN values detected in the DataFrame. Data cleaning may be required.")

    # Calculate correlation matrix
    correlation_matrix = data.corr()

    # Display the correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)

    # Visualize the correlation matrix
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    # plt.title('Correlation Matrix')
    # plt.show()

def scatter_plot_daily_returns(api_key, crypto_symbol, stock_symbol, days=30):
    # Get historical prices for cryptocurrency
    crypto_history_data = get_historical_prices(api_key, crypto_symbol, days)
    crypto_prices = np.array(crypto_history_data.get('prices', [])).astype(float)
    crypto_returns = calculate_daily_returns(crypto_prices)

    # Get historical prices for the stock index
    stock_history_data = get_historical_prices(api_key, stock_symbol, days)
    stock_prices = np.array(stock_history_data.get('prices', [])).astype(float)
    stock_returns = calculate_daily_returns(stock_prices)

    # Create a scatter plot
    # plt.figure(figsize=(10, 6))
    # sns.scatterplot(x=crypto_returns, y=stock_returns)
    # plt.xlabel(f'{crypto_symbol} Returns')
    # plt.ylabel(f'{stock_symbol} Returns')
    # plt.title(f'Scatter Plot of Daily Returns ({days} days)')
    # plt.show()

    return crypto_returns, stock_returns