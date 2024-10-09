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


if __name__ == "__main__":
    app.run(debug=True)