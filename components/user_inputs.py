import requests

def get_symbol_input():
    while True:
        crypto_symbol = input("Enter the cryptocurrency symbol (e.g., bitcoin): ").lower()
        if crypto_symbol.isalpha():
            response = requests.get(f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}')
        
            if response.status_code == 200:
                break
            else:
                print(f"Invalid cryptocurrency symbol. Please enter a valid symbol.")
                continue
        else:
            print("Invalid input. Please enter a valid cryptocurrency symbol.")

    return crypto_symbol

def get_days_input():
    while True:
        try:
            days = int(input("Enter the number of days for historical price analysis: "))
            if days > 0:
                break
            else:
                print("Invalid input. Please enter a positive integer for the number of days.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of days.")

        return days