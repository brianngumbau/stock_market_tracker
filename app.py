from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from stock_api import get_stock_data
from dotenv import load_dotenv
import os
from forms import RegistrationForm, LoginForm
import bcrypt

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
    stock_data = {
            "symbol": request.form.get('symbol'),
            "company_name": request.form.get('company_name'),
            "open": request.form.get('open'),
            "close": request.form.get('close'),
            "high": request.form.get('high'),
            "low": request.form.get('low'),
            "volume": request.form.get('volume')
        }
    
    users_collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"watchlist": stock_data}}
    )
    flash(f"Stock {stock_data['symbol']} has been added to your watchlist!", 'success')
    return redirect(url_for('home'))

@app.route('/watchlist', methods=['GET'])
def watchlist():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = users_collection.find_one({"_id": user_id})

    if user and "watchlist" in user:
        watchlist = user["watchlist"]
    else:
        watchlist = []

    return render_template('watchlist.html', watchlist=watchlist)

@app.route('/remove', methods=['POST'])
def remove_from_watchlist():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    symbol = request.form.get('symbol')

    users_collection.update_one(
        {"_id": user_id},
        {"$pull": {"watchlist": {"symbol": symbol}}}
    )

    flash(f"Stock {symbol} has been removed from your watchlist.", 'success')
    return redirect(url_for('watchlist'))


if __name__ == "__main__":
    app.run(debug=True)