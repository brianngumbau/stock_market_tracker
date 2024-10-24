Stock Market Tracker

A web application that allows users to track stock prices, view stock charts, and manage a personalized watchlist. This project is part of a web development portfolio, utilizing Python (Flask) for the back-end, MongoDB for data storage, and Bootstrap for the front-end.

Features
User Authentication: Secure registration and login with password hashing.

Stock Search: Search for stocks by symbol and view detailed information including price, percentage change, and market trends.

Watchlist Management: Add stocks to a personalized watchlist for easy tracking.

Stock Chart: View interactive stock charts for searched stocks.

Market Trends (Work in Progress): Analyzing stock market trends based on user-selected stocks.

Responsive Design: Front-end built with Bootstrap to ensure mobile compatibility.

Technologies Used
Back-end: Flask (Python)
Front-end: Bootstrap, HTML, CSS
Database: MongoDB Atlas
APIs:
yfinance for stock data
Possible integration with other APIs like Alpha Vantage or Finnhub for more detailed data
Form Handling: Flask-WTF for handling forms (user registration, login, etc.)
Data Storage:
User information (authentication) and watchlist stored in MongoDB Atlas.

Installation

Clone the repository:

git clone https://github.com/brianngumbau/stock-market-tracker.git
cd stock-market-tracker

Create a virtual environment:

python -m venv venv

Activate the virtual environment:
On macOS/Linux:

source venv/bin/activate

On Windows:

venv\Scripts\activate

Install the required dependencies:
pip install -r requirements.txt

Set up environment variables: Create a .env file and add your MongoDB URI, Flask secret key, and any API keys.

FLASK_SECRET_KEY=your_secret_key
MONGO_URI=your_mongo_db_uri

Run the application:

flask run

Open the app in your browser:
http://127.0.0.1:5000/


Usage

Sure! Here’s a sample README.md template for your Stock Market Tracker project. You can customize it based on your specific features, implementation, and tools used.

Stock Market Tracker
A web application that allows users to track stock prices, view stock charts, and manage a personalized watchlist. This project is part of a web development portfolio, utilizing Python (Flask) for the back-end, MongoDB for data storage, and Bootstrap for the front-end.

Features
User Authentication: Secure registration and login with password hashing.
Stock Search: Search for stocks by symbol and view detailed information including price, percentage change, and market trends.
Watchlist Management: Add stocks to a personalized watchlist for easy tracking.
Stock Chart: View interactive stock charts for searched stocks.
Market Trends (Work in Progress): Analyzing stock market trends based on user-selected stocks.
Responsive Design: Front-end built with Bootstrap to ensure mobile compatibility.
Technologies Used
Back-end: Flask (Python)
Front-end: Bootstrap, HTML, CSS
Database: MongoDB Atlas
APIs:
yfinance for stock data
Possible integration with other APIs like Alpha Vantage or Finnhub for more detailed data
Form Handling: Flask-WTF for handling forms (user registration, login, etc.)
Data Storage:
User information (authentication) and watchlist stored in MongoDB Atlas.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/stock-market-tracker.git
cd stock-market-tracker
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On macOS/Linux:
bash
Copy code
source venv/bin/activate
On Windows:
bash
Copy code
venv\Scripts\activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: Create a .env file and add your MongoDB URI, Flask secret key, and any API keys.

bash
Copy code
FLASK_SECRET_KEY=your_secret_key
MONGO_URI=your_mongo_db_uri
Run the application:

bash
Copy code
flask run
Open the app in your browser:

arduino
Copy code
http://127.0.0.1:5000/
Usage
Search for Stocks
Enter the stock symbol in the search bar to get the latest data for a specific stock.
Manage Watchlist
After searching for a stock, click the "Add to Watchlist" button to save it. View and manage your watchlist from the user dashboard.
View Stock Chart
Click "View Chart" to see a detailed chart of the stock's price movement over time.
Authentication
Register as a new user to access the watchlist and personalized stock data features.
Login to access your saved watchlist and stock preferences.
Future Improvements
Market Trends Analysis: Provide more insights into stock market trends based on user data.
Enhanced Charting: Add more interactive features to stock charts like zooming, custom date ranges, etc.
Real-Time Data: Integrate with a real-time stock data API for live updates.
License
This project is licensed under the MIT License. See the LICENSE file for details.