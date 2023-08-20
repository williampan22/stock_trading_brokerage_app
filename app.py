import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from stock_functions import quote_stock, get_stock_price_history, chart_stock_price
from login import require_login
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
# app.permanent_session_lifetime = None
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
            return jsonify({'error': 'Username, password, and confirmation password cannot be blank.'}), 400
        # If password does not match password confirmation return error
        if password != confirm_password: 
            return jsonify({'error': 'Passwords do not match. Ensure that the password matches the confirmation password.'}), 400
        # If username already exists return error
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
        if user: 
            return jsonify({'error': 'Username already exists. Plesae choose a new username.'}), 400
        # Hash password for privacy
        hash_password = generate_password_hash(password)    
        # Create user and add to database
        user = User(username=username, hash_password=hash_password, cash=0)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registered Successfully.'}), 200
    else: 
        return render_template("register.html", active_page="register")

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
            return jsonify({'error': 'Username and password cannot be blank'}), 400

        # SELECT username from database and return error if password does not match
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

        if not user:
            return jsonify({'error': 'Invalid username or password'}), 400

        if not check_password_hash(user.hash_password, password):
            return jsonify({'error': 'Invalid username or password'}), 400

        # Log user in with session_id
        session["user_id"] = user.id
        return jsonify({'message': 'Login Successful.'}), 200
    else:
        return render_template("login.html", active_page='login')

# Log user out
@app.route("/logout")
@require_login
def logout():
    session.clear()
    return redirect("/login")

# Features
@app.route("/features")
def features():
    session.clear()
    return render_template("features.html", active_page="features")

# Features
@app.route("/about")
def about():
    session.clear()
    return render_template("about.html", active_page="about")

# Clear Flask User Session after close browser
@app.route('/clear_session')
def clear_session():
    session.clear()

# Show Portfolio in Index (Home) Page 
@app.route("/")
@require_login
def index(): 
    API_LIMIT_REACHED = False
    portfolio = db.session.execute(db.select(Portfolio).filter_by(user_id=session["user_id"])).scalars()
    user = db.one_or_404(db.select(User).filter_by(id=session["user_id"]))
    current_cash = round(user.cash, 2)
    for row in portfolio: 
        symbol = row.symbol
        quote = quote_stock(symbol, API_KEY)
        print(quote)
        if "code" in quote and quote["code"] == 429: 
            API_LIMIT_REACHED = True
        else: 
            current_price = float(quote["close"])
            change = float(quote["change"])
            percent_change = float(quote["percent_change"])
            avg_buy_price = row.avg_buy_price
            shares = row.shares
            initial_total_cost = round(avg_buy_price*shares, 2)
            total_value = round(current_price*shares, 2)
            profit_loss = round(total_value - initial_total_cost, 2)
            profit_loss_percent = round(profit_loss/initial_total_cost, 4)
            profit_loss_day = round(change*shares, 2) 
            profit_loss_percent_day = round(percent_change, 4)
            row.initial_total_value = initial_total_cost
            row.total_value = total_value
            row.current_price = round(current_price, 2)
            row.profit_loss = profit_loss
            row.profit_loss_percent = profit_loss_percent
            row.profit_loss_day = profit_loss_day
            row.profit_loss_percent_day = profit_loss_percent_day
            db.session.commit()
    portfolio = db.session.execute(db.select(Portfolio).filter_by(user_id=session["user_id"])).scalars()
    return render_template("index.html", portfolio=portfolio, current_cash=current_cash, active_page='portfolio', API_LIMIT_REACHED=API_LIMIT_REACHED)

# Show Trade History
@app.route("/trade_history")
@require_login
def trade_history(): 
    trade_history = db.session.execute(db.select(Trade_History).filter_by(user_id=session["user_id"])).scalars()
    return render_template("trade_history.html", trade_history=trade_history, active_page='trade_history')

# Deposit Money Into Account
@app.route("/deposit", methods=["GET","POST"])
@require_login
def depsoit(): 
    if request.method == "POST": 
        cash_to_deposit = request.form.get("cash_to_deposit")
        user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one_or_none()
        current_cash = round(user.cash, 2)
        new_cash = round(current_cash + float(cash_to_deposit), 2)
        user.cash = new_cash
        db.session.commit()
        return redirect("/")
    else: 
        user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one_or_none()
        current_cash = user.cash
        return render_template("deposit.html", current_cash=current_cash, active_page='deposit')

# Quote Stock 
@app.route("/quote", methods=["GET", "POST"])
@require_login
def quote():
    symbol = ""
    show_quote_info = False
    preloaded_symbol = request.args.get("symbol")
    if preloaded_symbol: 
        symbol = preloaded_symbol
        show_quote_info = True
    if request.method == "POST" or show_quote_info:
        preloaded_symbol = request.args.get("symbol")
        symbol = preloaded_symbol
        if not symbol:
            symbol = request.form.get("symbol")            
        quote = quote_stock(symbol, API_KEY)
        fig = chart_stock_price(symbol, "1day", 1000)
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        stock_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return render_template("quoted_show_info.html", quote=quote, stock_chart=stock_chart)
    else:
        return render_template("quote.html", active_page='quote')

# Buy Stock
@app.route("/buy", methods=["GET","POST"])
@require_login
def buy(): 
    if request.method == "POST": 
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = quote_stock(symbol, API_KEY)

        if not quote: 
            return jsonify({'error': 'Invalid Stock Ticker. Please Enter a Valid Stock Ticker'}), 400
        
        symbol = quote["symbol"]
        name = quote["name"]
        current_price = round(float(quote["close"]), 2)
        total_cost = round(current_price * shares, 2)
        user = db.one_or_404(db.select(User).filter_by(id=session["user_id"]))
        current_cash = user.cash

        if current_cash < total_cost:
            return jsonify({'error': 'Insufficient funds to buy the shares.'}), 400
        
        new_cash = current_cash - total_cost
        user.cash = new_cash
        is_stock_already_owned = db.session.execute(db.select(Portfolio).filter_by(user_id=session["user_id"], symbol=symbol)).scalar_one_or_none()

        if not is_stock_already_owned:
            portfolio_trade = Portfolio(user_id=session["user_id"], symbol=symbol, name=name, shares=shares, avg_buy_price=current_price, total_value=total_cost)
            db.session.add(portfolio_trade)
        else: 
            current_shares = is_stock_already_owned.shares
            new_shares = current_shares + shares
            new_value = new_shares * current_price
            is_stock_already_owned.shares = new_shares
            is_stock_already_owned.total_value = new_value 

        trade_history_trade = Trade_History(user_id=session["user_id"], order_type="BUY", order_price=current_price, symbol=symbol, shares=shares, total_value=total_cost, time=datetime.now())
        db.session.add(trade_history_trade)
        db.session.commit()
        return jsonify({'message': 'Shares bought successfully.'}), 200
    
    else: 
        return render_template("buy.html", active_page='buy')


# Sell Stock 
@app.route("/sell", methods=["GET", "POST"])
@require_login
def sell():
    if request.method == "POST":
        symbol_to_sell = request.form.get("symbol").upper()
        shares_to_sell = int(request.form.get("shares"))
        stock_to_sell = db.session.execute(db.select(Portfolio).filter_by(user_id=session["user_id"], symbol=symbol_to_sell)).scalar_one_or_none()

        if not stock_to_sell:
            return jsonify({'error': 'Stock not found in your portfolio.'}), 400

        shares_owned = stock_to_sell.shares

        if shares_to_sell > shares_owned:
            return jsonify({'error': 'You cannot sell more shares than you currently own. Invalid number of shares'}), 400
        
        if shares_to_sell < 0:
            return jsonify({'error': 'You cannot sell a negative amount of shares. Invalid number of shares'}), 400

        shares_left = shares_owned - shares_to_sell

        if shares_left > 0:
            stock_to_sell.shares = shares_left
        elif shares_left == 0:
            db.session.delete(stock_to_sell)

        quote = quote_stock(symbol_to_sell, API_KEY)

        if not quote:
            return jsonify({'error': 'Error fetching stock quote.'}), 400

        symbol = quote["symbol"]
        current_price = round(float(quote["close"]), 2)
        total_value = round(current_price * shares_to_sell, 2)

        user = db.one_or_404(db.select(User).filter_by(id=session["user_id"]))
        current_cash = user.cash
        new_cash = current_cash + total_value
        user.cash = new_cash

        trade_history_trade = Trade_History(user_id=session["user_id"], order_type="SELL", order_price=current_price, symbol=symbol, shares=shares_to_sell, total_value=total_value, time=datetime.now())
        db.session.add(trade_history_trade)
        db.session.commit()

        return jsonify({'message': 'Shares sold successfully.'}), 200

    else:
        portfolio = db.session.execute(db.select(Portfolio).filter_by(user_id=session["user_id"])).scalars()
        return render_template("sell.html", portfolio=portfolio, active_page='sell')
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
    current_price = db.Column(db.Float, nullable=True)
    initial_total_value = db.Column(db.Float, nullable=True)
    total_value = db.Column(db.Float, nullable=False)
    profit_loss = db.Column(db.Float, nullable=True)
    profit_loss_percent = db.Column(db.Float, nullable=True)
    profit_loss_day = db.Column(db.Float, nullable=True)
    profit_loss_percent_day = db.Column(db.Float, nullable=True)
    
# History model
class Trade_History(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    order_price = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

# run in terminal to initalize database: 
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()

if __name__ == '__main__':
    app.run(debug=True)