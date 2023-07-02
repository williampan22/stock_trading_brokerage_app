import os
from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from stock_functions import quote_stock

load_dotenv() 
API_KEY = os.getenv('API_KEY') 

app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname("trading_brokerage_app/app.py"))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tradingApp.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tradingApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if (not username or not password or not confirm_password): 
            print("1")
            return redirect("/register"), 400
        if password != confirm_password: 
            print("2")
            return redirect("/register"), 400
        # reminder - check if username is in database
        hash_password = generate_password_hash(password)    
        user = User(username=username, hash_password=hash_password, cash=0)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    else: 
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # session.clear() 
    if request.method == "POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password: 
            return redirect("/login"), 400
        
    else: 
        return render_template("login.html")
    



@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/buy", methods=["GET","POST"])
def buy (): 
    if request.method == "POST": 
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = quote_stock(symbol, API_KEY)
        if not quote: 
            return redirect("/buy"), 400
        symbol = quote["symbol"]
        name = quote["name"]
        current_price = quote["close"]
        total_value = current_price * shares
        return quote

        # will finish later
    else: 
        return render_template("buy.html")

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    cash = db.Column(db.Float, default=0.0, nullable =False)

# Portfolio model
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    avg_buy_price = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    total_gain = db.Column(db.Float, nullable=False)
    total_gain_percent = db.Column(db.Float, nullable=False)

# History model
class Transaction_History(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)
    order_price = db.Column(db.Float, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

# run in terminal to initalize database: 
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()

if __name__ == '__main__':
    app.run(debug=True)