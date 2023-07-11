import os
import requests
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import json


# load os to get secret api_key from .env protected by .gitignore
load_dotenv() 
API_KEY = os.getenv('API_KEY') 

# def main(): 
#     print(get_stock_quote(ticker, API_KEY))

# returns info for one stock in a dictionary
def quote_stock(ticker_symbol, API_KEY):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={API_KEY}"
    stock_data =  requests.get(url).json() 
    return stock_data

def stock_price_history(ticker_symbol, interval, API_KEY): 
    url = f"https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval={interval}&dp=2&order=ASC&apikey={API_KEY}"
    stock_data = requests.get(url).json()
    return stock_data["values"]

data = stock_price_history("CLX", "1min", API_KEY)
# print(json.dumps(data, indent=4))
df = pd.DataFrame.from_records(data)
print(df)
df["datetime"] = pd.to_datetime(df["datetime"])

fig, ax = plt.subplots()

ax.plot(df['datetime'], df['close'])
ax.tick_params(axis='x', labelsize=5)
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price')
ax.set_title('Stock Chart')
plt.xticks(rotation=45)
plt.savefig('plot.png')
