import requests
from datetime import datetime
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_real_time_price(api_key, crypto_symbol):
    base_url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': crypto_symbol, 'vs_currencies': 'eur'}
    headers = {'Authorization': f'Bearer {api_key}'}
    
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data[crypto_symbol]['eur']
    else:
        print(f"Error fetching real-time price. Status code: {response.status_code}")
        return None

def update_real_time_price_chart(api_key, crypto_symbol, prices, times):
    while True:
        real_time_price = get_real_time_price(api_key, crypto_symbol)

        if real_time_price is not None:
            # Append the new price and timestamp
            prices.append(real_time_price)
            times.append(datetime.now())

        time.sleep(10)

def live_price(api_key, crypto_symbol):
    # Initialize lists to store price and timestamp data
    prices = []
    times = []

    # Start the thread for updating real-time price
    rt_thread = threading.Thread(target=update_real_time_price_chart, args=(api_key, crypto_symbol, prices, times))
    rt_thread.daemon = True
    rt_thread.start()

    # Set up the live price graph
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label='Live Price')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price (EUR)')
    ax.legend()

    def update_graph(frame):
        line.set_data(times, prices)
        ax.relim()
        ax.autoscale_view()

    ani = FuncAnimation(fig, update_graph, blit=False, cache_frame_data=False)
    plt.show()

    try:
        while True:
            print("Main program running...")
            time.sleep(10)
    except KeyboardInterrupt:
        # CTRL C
        print("Exiting program.")
