import matplotlib.pyplot as plt

def calculate_simple_moving_average(prices, window_size):
    sma = []
    for i in range(len(prices) - window_size + 1):
        window = prices[i : i + window_size]
        average = sum(window) / len(window)
        sma.append(average)
    return sma

def visualize_sma(prices, sma_values, window_size):
    plt.plot(range(window_size - 1, len(prices)), prices[window_size-1:], label='Bitcoin Prices')
    plt.plot(range(window_size - 1, len(prices)), sma_values, label=f'SMA ({window_size} days)')
    plt.xlabel('Days')
    plt.ylabel('Price (EUR)')
    plt.title('Historical Prices and Simple Moving Average for Bitcoin')
    plt.legend()
    plt.show()

def show_sma(prices):
    window_size = 7
    sma_values = calculate_simple_moving_average(prices, window_size)

    print(f"Simple Moving Averages (Window Size: {window_size}):")
    for i, value in enumerate(sma_values, start=1):
        print(f"Day {i}: {value} EUR")
    visualize_sma(prices, sma_values, window_size)