import os
import requests
from dotenv import load_dotenv

ticker = "AAPL"

# load os to get secret api_key from .env protected by .gitignore
load_dotenv() 
API_KEY = os.getenv('API_KEY') 

def main(): 
    print(get_stock_quote(ticker, API_KEY))

def get_stock_quote(ticker_symbol, API_KEY):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={API_KEY}"
    response =  requests.get(url).json()
    return response
    

main()