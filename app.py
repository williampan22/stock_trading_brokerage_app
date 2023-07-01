from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tradingApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/buy", methods=["GET","POST"])
def buy (): 
    if request.method == "POST": 
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        return symbol
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