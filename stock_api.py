import requests
# from polygon import RESTClient
import yfinance as yf
from datetime import datetime

# API_KEY = "KPLKMjstKCqFHRi9tZUE1OshfYardCEt"
# BASE_URL = "https://api.polygon.io"
# client = RESTClient(API_KEY)

date = datetime.now().strftime("%Y-%m-%d")
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        # stock_data = stock.history(period="1d")
        if stock_info:
            return {
                'symbol': stock_info['symbol'],
                'company_name': stock_info.get('shortName', 'N/A'),
                'open': stock_info.get('open', 'N/A'),
                'close': stock_info.get('previousClose', 'N/A'),
                'high': stock_info.get('dayHigh', 'N/A'),
                'low': stock_info.get('dayLow', 'N/A'),
                'volume': stock_info.get('volume', 'N/A'),
            }
        else:
            return {'error': 'No data available for this symbol'}
    except Exception as e:
        print(f"Error fetching stock data: {e}")

# print(get_stock_data('AAPL'))