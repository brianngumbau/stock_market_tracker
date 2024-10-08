from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from stock_api import get_stock_data
from dotenv import load_dotenv
import os
from forms import RegistrationForm, LoginForm
import bcrypt

load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

client = MongoClient(os.getenv("MONGO_URI"))
db = client['stock_market_tracker']
stocks_collection = db['stocks']
users_collection = db['users']

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password.decode('utf-8')
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
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user['password'].encode('utf-8')):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', form=form)

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