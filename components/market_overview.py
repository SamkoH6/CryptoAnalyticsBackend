import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_market_overview(api_key):
    base_url = 'https://api.coingecko.com/api/v3/'
    response_market = requests.get(f'{base_url}global')
    if response_market.status_code == 200:
        # Converts the JSON to a Python dictionary
        market_data = response_market.json()
        return market_data
    else:
        print(f"Error fetching market overview. Status code: {response_market.status_code}")
        print(response_market.text)
        return None

def print_market_overview(market_data):
    print("Market Overview:")
    print(f"Total Market Cap: {market_data['data']['total_market_cap']['eur']} eur")
    print(f"Total 24h Volume: {market_data['data']['total_volume']['eur']} eur")
    print(f"Bitcoin Percentage: {market_data['data']['market_cap_percentage']['btc']}%")

def get_historical_prices(api_key, crypto_symbol, days=30):
    base_url = 'https://api.coingecko.com/api/v3/'
    history_endpoint = f'coins/{crypto_symbol}/market_chart'
    history_params = {'vs_currency': 'eur', 'days': str(days), 'interval': 'daily'}
    history_response = requests.get(f'{base_url}{history_endpoint}', params=history_params)
    history_data = history_response.json()
    return history_data

def get_dates_and_days(timestamps):
    # Getting rid of the timestamp, to just leave the price
    prices = [price[1] for price in timestamps]

    # Converting the milliseconds into dates and days of the week
    dates_and_days = [
        (datetime.fromtimestamp(timestamp[0] / 1000).strftime('%Y-%m-%d'),
         datetime.fromtimestamp(timestamp[0] / 1000).strftime('%A'))
        for timestamp in timestamps
    ]

    # Create a dictionary to store unique date-day pairs and their corresponding prices
    unique_dates_and_days = {}
    for (date, day), price in zip(dates_and_days, prices):
        if (date, day) not in unique_dates_and_days:
            unique_dates_and_days[(date, day)] = price

    return unique_dates_and_days

def print_historical_prices(unique_dates_and_days):
    # Print the unique date-day pairs and their corresponding prices
    for (date, day), price in unique_dates_and_days.items():
        print(f"{date} ({day}): {price} EUR")


def visualize_historical_prices(prices):
    # Create a line chart, using Matplotlib
    plt.plot(prices, label='Bitcoin Prices')
    plt.xlabel('Days')
    plt.ylabel('Price (EUR)')
    plt.title('Historical Prices for Bitcoin')
    plt.legend()
    plt.show()

def visualize_profits(differences):
    # Extracting days and profits for plotting
    days = list(differences.keys())
    profits = [sum(price_diff_list) for price_diff_list in differences.values()]

    # Creating a bar chart
    plt.bar(days, profits, color=['green' if profit >= 0 else 'red' for profit in profits])
    plt.xlabel('Days')
    plt.ylabel('Profit (EUR)')
    plt.title('Profits for Each Day')
    plt.show()

def largest_divisor_less_than_x(x):
    for num in range(x - 1, 0, -1):
        if num % 7 == 0:
            return num
    return None

def week_spikes(history_data):
    if history_data is None or 'prices' not in history_data:
        print("Error fetching historical prices.")
        return
    timestamps = history_data.get('prices', [])

    data = get_dates_and_days(timestamps)

    number = largest_divisor_less_than_x(len(data))
    data = dict(list(data.items())[:number])


    last_price = None
    differences = {}
    differences["Monday"] = []
    differences["Tuesday"] = []
    differences["Wednesday"] = []
    differences["Thursday"] = []
    differences["Friday"] = []
    differences["Saturday"] = []
    differences["Sunday"] = []
    for (date, day), price in data.items():

        if last_price is not None:
            differences[day].append(price - last_price)
        last_price = price

    for day, price_diff_list in differences.items():
        print(f"{day}: {price_diff_list}")

    biggest_profit = 0
    lowest_profit = float('inf')

    for day, price_diff in differences.items():
        day_sum = sum(price_diff)
        print(f"{day}: {day_sum}")
        if day_sum > biggest_profit:
            biggest_profit = day_sum
            biggest_profit_day = day

        if day_sum < lowest_profit:
            lowest_profit = day_sum
            lowest_profit_day = day

    print(f"The day with the biggest overall profit was {biggest_profit_day}: {biggest_profit}")
    print(f"The day with the lowest overall profit was {lowest_profit_day}: {lowest_profit}")

    return differences

def calculate_market_cap_changes(market_data, currency1='usd', currency2='eur'):
    try:
        market_caps = market_data['data']['total_market_cap']

        if currency1 not in market_caps or currency2 not in market_caps:
            raise KeyError(f"Market caps for {currency1} or {currency2} not found in market_data.")

        cap1 = market_caps[currency1]
        cap2 = market_caps[currency2]

        percentage_change = ((cap2 - cap1) / cap1) * 100

        return percentage_change

    except KeyError as e:
        print(f"Error: {e}")
        return None