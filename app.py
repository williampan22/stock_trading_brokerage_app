import os
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from stock_functions import quote_stock
from login import require_login

# Hides secret api key 
load_dotenv() 
API_KEY = os.getenv('API_KEY') 
SECRET_KEY = os.getenv('SECRET_KEY')

# Starts and initiates flask app + session
# Flask session is set to file-system instead of on server with cookies - easier to handle on local development
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tradingApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect database
db = SQLAlchemy(app)

# No cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Register for an account
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Get password and username from HTML form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # If username, password, or password confirmation is blank (from inspect element) return error
        if (not username or not password or not confirm_password): 
            return redirect("/register"), 400
        # If password does not match password confirmation return error
        if password != confirm_password: 
            return redirect("/register"), 400
        # If username already exists return error
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
        if user: 
            return redirect("/register"), 400
        # Hash password for privacy
        hash_password = generate_password_hash(password)    
        # Create user and add to database
        user = User(username=username, hash_password=hash_password, cash=0)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    else: 
        return render_template("register.html")

# Login into account
@app.route("/login", methods=["GET", "POST"])
def login():

    # Clear session_id to enforce log-in
    session.clear() 

    if request.method == "POST": 
        # Get username and password from HTML form
        username = request.form.get("username")
        password = request.form.get("password")
        # If username or password is blank (from inspect element) return error
        if not username or not password: 
            return redirect("/login"), 403
        # SELECT username from database and return error if password does not match 
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
        if not user: 
            return redirect("/login"), 404
        if not check_password_hash(user.hash_password, password): 
            return redirect("/login"), 403
        # Log user in with session_id
        session["user_id"] = user.id
        return redirect("/")
    else: 
        return render_template("login.html")

# Log user out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@require_login
@app.route("/")
def index(): 
    return render_template("index.html")

@require_login
@app.route("/deposit")
def depsoit(): 
    cash_to_deposit = request.form.get("cash_to_deposit")
    user = db.session.execute(db.select(User).filter_by(username=session["user_id"])).scalar_one_or_none()
    currnet_cash = user.cash
    new_cash = currnet_cash + cash_to_deposit
    user.cash = new_cash
    db.session_commit()
    return render_template("deposit.html")

@app.route("/buy", methods=["GET","POST"])
def buy(): 
    if request.method == "POST": 
        symbol = request.form.get("symbol")
        shares_string = request.form.get("shares")
        quote = quote_stock(symbol, API_KEY)
        if not quote: 
            return redirect("/buy"), 400
        try:
            shares_int = int(shares_string)
            shares = shares_int
        except ValueError:
            print("The string is not an integer.")
            return redirect("/buy"), 400
        # symbol = quote["symbol"]
        # name = quote["name"]
        # current_price = quote["close"]
        # total_cost = current_price * shares
        # user = db.one_or_404(db.select(User).filter_by(username=session["user_id"]))
        # currnet_cash = user.cash
        # if currnet_cash < total_cost:
        #     return redirect("/buy"), 400
        # new_cash = currnet_cash - total_cost
        # user.cash = new_cash
        # db.session.commit()
        return redirect("/")

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