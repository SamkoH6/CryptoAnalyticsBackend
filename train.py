from components.price_prediction import *
from components.market_overview import *
from tensorflow.keras.models import load_model
import json

MODEL_FILE = 'lstm_model.keras'

def generate_prediction(prices):
    scaler, prices_scaled = preprocess_data(np.array(prices))
    lstm_model = train_lstm_model(prices_scaled, lookback_window=30, epochs=100, batch_size=30)
    lstm_model.save(MODEL_FILE)
    # lstm_predictions_scaled = predict_prices_lstm(lstm_model, prices_scaled, lookback_window=30, num_days=30)
    # predictions = scaler.inverse_transform(np.array(lstm_predictions_scaled).reshape(-1, 1))
    return lstm_model

def load_data(file_path):
    with open(file_path, 'r') as file:
        market_data = json.load(file)
    return market_data

history_data = load_data("history_data.txt")

if history_data is not None:
    timestamps = history_data.get('prices', [])

    ddp = get_dates_and_days(timestamps)
    prices = list(ddp.values())


    generate_prediction(prices)

    model = load_model(MODEL_FILE)