import requests
# from polygon import RESTClient
from datetime import datetime

API_KEY = "KPLKMjstKCqFHRi9tZUE1OshfYardCEt"
BASE_URL = "https://api.polygon.io"
# client = RESTClient(API_KEY)


stock_data = []
date = datetime.now().strftime("%Y-%m-%d")
def get_stock_data(symbol):
    OPEN_CLOSE_URL = f"{BASE_URL}/v1/open-close/{symbol}/{date}"
    params = {
        "adjusted": "true",
        "apikey": API_KEY
    }
    try:
        open_response = requests.get(OPEN_CLOSE_URL, params=params)
        if open_response.status_code == 200:
            print("Response Data:", open_response.json())
        else:
            print(f"Error {open_response.status_code}: {open_response.text}")
    except Exception as e:
        print(e)

get_stock_data("AAPL")