from components.market_overview import *
from components.live_price import *
from components.user_inputs import *
from components.sma import *
from components.correlation import *
from components.volatility import *
from components.price_prediction import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()
api_key = os.getenv("API_KEY")

def refresh_api_data(api_key, crypto_symbol, days):
    market_data = get_historical_prices(api_key, crypto_symbol, days)

    if market_data is not None:
    
        with open("history_data.txt", 'w') as file:
            json.dump(market_data, file)
        
        if market_data is not None:
            timestamps = market_data.get('prices', [])

            ddp = get_dates_and_days(timestamps)
            prices = list(ddp.values())
            prediction = generate_prediction(prices).tolist()
            with open("prediction_data.txt", 'w') as file:
                json.dump(prediction, file)

    return market_data

def load_data(file_path):
    with open(file_path, 'r') as file:
        market_data = json.load(file)
    return market_data

def generate_prediction(prices):
    scaler, prices_scaled = preprocess_data(np.array(prices))
    lstm_model = train_lstm_model(prices_scaled, lookback_window=30, epochs=100, batch_size=10)
    lstm_predictions_scaled = predict_prices_lstm(lstm_model, prices_scaled, lookback_window=30, num_days=30)
    predictions = scaler.inverse_transform(np.array(lstm_predictions_scaled).reshape(-1, 1))
    return predictions

def get_data_dict():
    history_data = load_data("history_data.txt")

    if history_data is not None:
        timestamps = history_data.get('prices', [])

        ddp = get_dates_and_days(timestamps)
        prices = list(ddp.values())
        week_data = week_spikes(history_data)

        window_size = 9
        sma = calculate_simple_moving_average(prices, window_size)

        volatility = calculate_volatility(np.array(prices))
        daily_returns = calculate_daily_returns(np.array(prices))
        
        predictions = load_data("prediction_data.txt")

        dict_items = list(ddp.items())
        last_updated = dict_items[-1][0][0]

        with open("current_coin.txt", 'r') as file:
            current_coin = file.read().strip()


        data_dict = {
            "prices": list(prices),
            "week_data": week_data,
            "sma": list(sma),
            "volatility": float(volatility),
            "daily_returns": list(daily_returns),
            "prediction": [num for inner_array in predictions for num in inner_array],
            "last_updated": last_updated,
            "current_coin": current_coin
        }

        return data_dict

    else:
        print("Market data is None")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        data_dict = get_data_dict()
        return jsonify(data=data_dict)
    elif request.method == 'POST':
        data = request.json
        refresh_api_data(api_key, data["cryptoSymbol"], data["cryptoDays"])
        current_coin = ''
        with open("current_coin.txt", 'w') as file:
            file.write(data["cryptoSymbol"])
        data_dict = get_data_dict()
        return jsonify(data=data_dict)

if __name__ == "__main__":
    app.run(debug=True)
