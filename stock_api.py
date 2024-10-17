import requests
# from polygon import RESTClient
import yfinance as yf
from datetime import datetime, timedelta

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

def get_historical_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        stock_history = stock.history(period=period)
        if not stock_history.empty:
            dates = stock_history.index.strftime('%Y-%m-%d').tolist()
            prices = stock_history['Close'].tolist()
            return {'dates': dates, 'prices': prices}
        else:
            return None
        
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None
    
def get_candlestick_data(symbol):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    stock_data = yf.download(symbol, start=start_date, end=end_date)

    if stock_data.empty:
        return None
    
    dates = stock_data.index.strftime('%Y-%m-%d').tolist() 
    opens = stock_data['Open'].tolist()
    highs = stock_data['High'].tolist()
    lows = stock_data['Low'].tolist()
    closes = stock_data['Close'].tolist()

    return {
        'dates': dates,
        'opens': opens,
        'highs': highs,
        'lows': lows,
        'closes': closes
    }