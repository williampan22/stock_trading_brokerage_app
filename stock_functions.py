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
    plt.savefig('plot.png', dpi=300)
    return fig

chart_stock_price("INTU", "1day", 1000)