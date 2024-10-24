from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from stock_api import get_stock_data, get_historical_data, get_candlestick_data
from dotenv import load_dotenv
import os
from forms import RegistrationForm, LoginForm
import bcrypt
from bson import ObjectId
import yfinance as yf
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['stock_market_tracker']
stocks_collection = db['stocks']
users_collection = db['users']

def is_logged_in():
    return 'user_id' in session


@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password.decode('utf-8'),
            "watchlist": []
        }
        users_collection.insert_one(user_data)
        flash("Your account has been created!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users_collection.find_one({"email": form.email.data})
        if user:
            if bcrypt.checkpw(form.password.data.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = str(user['_id'])
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('Email not registered. Please sign up.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('You have logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search_stock():
    symbol = request.form.get('symbol')
    stock_data = get_stock_data(symbol)
    if stock_data:
        return render_template('home.html', stock_data=stock_data)
    else:
        return render_template('home.html', error="No data found for the symbol")


@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    stock_symbol = request.form.get('symbol')
    stock_info = yf.Ticker(stock_symbol).info

    stock_data = {
            "symbol": stock_symbol,
            "company_name": request.form.get('company_name'),
            "open": request.form.get('open'),
            "close": request.form.get('close'),
            "high": request.form.get('high'),
            "low": request.form.get('low'),
            "volume": request.form.get('volume'),
            "current_price": stock_info.get('currentPrice', 0),
            "percent_change": stock_info.get('regularMarketChangePercent', 0),
            "last_updated": datetime.utcnow()
        }
    
    print(f"Adding stock for user {user_id}: {stock_data}")
    
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"watchlist": stock_data}}
    )
    flash(f"Stock {stock_data['symbol']} has been added to your watchlist!", 'success')
    return redirect(url_for('home'))

@app.route('/watchlist', methods=['GET'])
def watchlist():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    watchlist = user.get('watchlist', [])

    updated_watchlist = []

    for stock in watchlist:
        symbol = stock['symbol']

        try:
           stock_info = yf.Ticker(symbol)
           latest_data = stock_info.history(period="1d").iloc[0]

           current_price = latest_data['Close']
           previous_close = float(stock.get('close', current_price))
           percent_change = ((current_price - previous_close) / previous_close) * 100

           stock['current_price'] = round(current_price, 2)
           stock['percent_change'] = round(percent_change, 2)
           stock['last_updated'] = datetime.now()

        except Exception as e:
            print(f"Error updating stock {symbol}: {e}")
            stock['current_price'] = "N/A"
            stock['percent_change'] = "N/A"
            stock['last_updated'] = "N/A"

        updated_watchlist.append(stock)

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"watchlist": updated_watchlist}}
    )

    return render_template('watchlist.html', watchlist=watchlist)

@app.route('/remove', methods=['POST'])
def remove():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    symbol = request.form.get('symbol')

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"watchlist": {"symbol": symbol}}}
    )

    flash(f"Stock {symbol} has been removed from your watchlist.", 'success')
    return redirect(url_for('watchlist'))

@app.route('/view_chart', methods=['GET'])
def view_chart():
    symbol = request.args.get('symbol')
    candlestick_data = get_candlestick_data(symbol)

    if not candlestick_data:
        flash(f"Could not fetch chart data for {symbol}", "danger")
        return redirect(url_for('home'))
    
    print(candlestick_data)

    return render_template('chart.html', symbol=symbol, candlestick_data=candlestick_data)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)