import os
import requests
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from dotenv import load_dotenv

# load os to get secret api_key from .env protected by .gitignore
load_dotenv() 
API_KEY = os.getenv('API_KEY') 

# returns info for one stock in a dictionary
def quote_stock(ticker_symbol, API_KEY):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={API_KEY}"
    stock_data =  requests.get(url).json() 
    return stock_data

def get_stock_price_history(ticker_symbol, interval, outputsize): 
    url = f"https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval={interval}&dp=2&order=ASC&outputsize={outputsize}&apikey={API_KEY}"
    stock_data = requests.get(url).json()
    return stock_data["values"]

def chart_stock_price(ticker_symbol, interval, outputsize): 
    data = get_stock_price_history(ticker_symbol, interval, outputsize)
    df = pd.DataFrame.from_records(data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df['close'] = df['close'].astype(float)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['datetime'], df['close'], label="Stock Price", color="blue", linestyle='-', marker='o', markersize=3)

    ax.grid(linestyle='--', linewidth=0.5, alpha=0.7)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Calculate the y-axis limits as whole numbers
    y_min = math.floor(df['close'].min())
    y_max = math.ceil(df['close'].max())
    ax.set_ylim(y_min, y_max)

    # Set the y-axis tick locations
    # ax.yaxis.set_major_locator(MaxNLocator(nbins='auto', integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=20, integer=True))

    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Closing Price', fontsize=12)
    ax.set_title('Stock Price Chart of ' + ticker_symbol.upper(), fontsize=16)
    ax.tick_params(axis='both', labelsize=10)

    fig.set_facecolor('white')

    plt.tight_layout(pad=2)
    return fig

# Errors
# Twelve Data API uses a unified error response scheme. Consisting of a JSON object with code, message and status keys.

# HTTP request example

# https://api.twelvedata.com/time_series?symbol=AAPL&interval=0.99min&apikey=your_api_key
# This request with incorrect interval set will return JSON with the following structure

# {
#   "code": 400,
#   "message": "Invalid **interval** provided: 0.99min. Supported intervals: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month",
#   "status": "error"
# }
# Possible output error codes are:

# Error Code	Status	Meaning
# 400	Bad Request	There is an error with one or multiple parameters.
# 401	Unauthorized	Your API key is wrong or not valid.
# 403	Forbidden	Your API key is valid but has no permissions to make request available on the upper plans.
# 404	Not Found	The specified data can not be found.
# 414	Parameter Too Long	The parameter which accepts multiple values is out of range.
# 429	Too Many Requests	You've reached your API request limits.
# 500	Internal Server Error	There is an error on the server-side. Try again later.