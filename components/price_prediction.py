import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Load historical prices from a file (assuming a single-column text file)
# prices = np.loadtxt("prices.txt")

def preprocess_data(prices):
    # Scale prices between 0 and 1 using MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices_scaled = scaler.fit_transform(prices.reshape(-1, 1))
    return scaler, prices_scaled

def create_lstm_model(input_shape):
    # Build an LSTM model with two layers and one dense output layer
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    
    # Compile the model using Adam optimizer and mean squared error loss
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm_model(prices_scaled, lookback_window=30, epochs=100, batch_size=10):
    X, y = [], []

    # Create input sequences and target values for training
    for i in range(len(prices_scaled) - lookback_window):
        X.append(prices_scaled[i:i + lookback_window])
        y.append(prices_scaled[i + lookback_window])

    X, y = np.array(X), np.array(y)
    # Reshape input sequences to match LSTM input format (number_of_sequences, lookback_window, 1)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Create and train the LSTM model
    model = create_lstm_model(input_shape=(X.shape[1], 1))
    model.fit(X, y, epochs=epochs, batch_size=batch_size)
    return model

def predict_prices_lstm(model, prices_scaled, lookback_window, num_days):
    # Prepare the last part of the data for prediction
    inputs = prices_scaled[-lookback_window:]
    inputs = np.reshape(inputs, (1, inputs.shape[0], 1))

    predictions_scaled = []

    # Generate predictions for the specified number of days
    for _ in range(num_days):
        prediction_scaled = model.predict(inputs)
        predictions_scaled.append(prediction_scaled[0, 0])
        inputs = np.append(inputs[:, 1:, :], prediction_scaled.reshape(1, 1, 1), axis=1)

    return predictions_scaled

def visualize_predictions_lstm(prices, predictions_scaled, scaler):
    # Transform predicted prices back to the original scale
    predictions = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1))

    # Visualize true prices and predicted prices
    plt.plot(prices, label='True Prices')
    plt.plot(range(len(prices), len(prices) + len(predictions)), predictions, label='Predicted Prices')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('LSTM Model Predictions')
    plt.legend()
    plt.show()
