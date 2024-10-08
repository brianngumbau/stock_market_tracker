from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from stock_api import get_stock_data

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['stock_market_tracker']
stocks_collection = db['stocks']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search_stock():
    symbol = request.form.get('symbol')
    stock_data = get_stock_data(symbol)
    if stock_data:
        return render_template('home.html', stock_data=stock_data)
    else:
        return render_template('home.html', error="No data found for the symbol")


if __name__ == "__main__":
    app.run(debug=True)