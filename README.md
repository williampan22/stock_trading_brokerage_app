# Stock Trading Brokerage App 

## Technologies Used
* Python, Javascript, HTML, Bootstrap CSS
* Flask (web framework for Python)
* Flask Session - Managing Users Login Session (redirects user to login/register page if not logged in)
* SQL Database (SQLAlchemy Library) - Stores Uesr Data, Trade History, Portfolio
* TwelveData Stock API - Fetches Stock Price & Quotes Data
* Git, Github
* Matplotlit, Pandas, Datetime, Werkzeug Security

# Description

I created an imitation of a stock brokerage app where users can trade stocks and manage their portfolio. There are the following pages and respective actions: 

* Register: Register for an account. Must input a username, password, and password confirmation. Error message is presented if the username is already taken or the password does not match the password confirmation. 
* Login: Log into account. Must input a username and password. Error message is presented if username and password do not match a valid account. 
* Home Page/Portfolio: Shows users their portfolio and amount of cash. Portfolio is shown in a table consisting of symbols of stock owned, name of stock owned, number of shares, average cost/share, current price, initial price cost, total current value, total P/L, total P/L %, day P/L, and day P/L %. 
* Quote Stock: Quote a stock. Must input a valid stock ticker. Upon quoting, show stock quote information (name, symbol, exchange, open, high, low, close, etc) and price stock chart. Error message is presented if the stock ticker is not valid. 
* Buy: Buy a stock. Must input a stock ticker and amount of shares to buy. Error message is presented if the stock ticker is invalid, the number of shares is not a positive integer, or if there are insufficient funds to purchase stock. 
* Sell: Sell a stock. Shows a dropdown of all currently owned stocks and a form to input the number of shares to sell. Error message is presented if the number of shares to sell is more than currently owned or if the number is not a positive integer. 
* Trade History: View trade history of buying/selling stocks. Shows each trade and its order type (buy/sell), stock symbol, number of shares, order price, total value bought/sold, and time the trade occurred. 
* Deposit: Deposit cash. Input amount of cash in USD to deposit. Error message is presented if the amount of cash that the user wishes to deposit is less than 0. 
* Logout: Logs users out of their account and redirects to the login page. This automatically occurs if the user is not logged in already and tries to access any page other than register, login, or logout. 

