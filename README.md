# Stock Trading Brokerage App 

## Technologies Used
* Python, Javascript, HTML, Bootstrap CSS
* Flask (web framework for Python)
* Flask Session - Managing Users Login Session (redirects user to login/register page if not logged in)
* SQL Database (SQLAlchemy Library) - Stores User Data, Trade History, Portfolio
* TwelveData Stock API - Fetches Stock Price & Quotes Data
* Git, Github
* Matplotlit, Pandas, Datetime, Werkzeug Security

## Description
I created an imitation of a stock brokerage app where users can trade stocks and manage their portfolio. There are the following pages and respective actions: 

* **Register**: Register for an account. Must input a username, password, and password confirmation. Error message is presented if the username is already taken or the password does not match the password confirmation.

_Register Form_

[![Screenshot-2023-08-20-112541.png](https://i.postimg.cc/3NyC02xc/Screenshot-2023-08-20-112541.png)](https://postimg.cc/xN2bWJHv)

_Error Message_

[![Screenshot-2023-08-20-112614.png](https://i.postimg.cc/59GmdKPd/Screenshot-2023-08-20-112614.png)](https://postimg.cc/MX7B152d)

* **Login**: Log into account. Must input a username and password. Error message is presented if username and password do not match a valid account.

_Login Form_

[![Screenshot-2023-08-20-112426.png](https://i.postimg.cc/QxTJXgPB/Screenshot-2023-08-20-112426.png)](https://postimg.cc/YhtWRFtk)

_Error Message_

[![Screenshot-2023-08-20-112503.png](https://i.postimg.cc/rsvG1zdF/Screenshot-2023-08-20-112503.png)](https://postimg.cc/fSf0Zzj6)

* **Home Page/Portfolio**: Shows users their portfolio and amount of cash. Portfolio is shown in a table consisting of symbols of stock owned, name of stock owned, number of shares, average cost/share, current price, initial price cost, total current value, total P/L, total P/L %, day P/L, and day P/L %.

[![Screenshot-2023-08-20-112750.png](https://i.postimg.cc/YCQRxNzc/Screenshot-2023-08-20-112750.png)](https://postimg.cc/QFxc8TzS)
[![Screenshot-2023-08-20-112740.png](https://i.postimg.cc/0QyCxTRx/Screenshot-2023-08-20-112740.png)](https://postimg.cc/PL0DQF5F)

* **Quote Stock**: Quote a stock. Must input a valid stock ticker. Upon quoting, show stock quote information (name, symbol, exchange, open, high, low, close, etc) and price stock chart. Error message is presented if the stock ticker is not valid.

_Quote Stock Form_

[![Screenshot-2023-08-20-112808.png](https://i.postimg.cc/c4pTYkYM/Screenshot-2023-08-20-112808.png)](https://postimg.cc/ZCLrzcwC)

_Upon Valid Stock Ticker, Show Quoted Stock Data & Stock Chart_

[![Screenshot-2023-08-20-112910.png](https://i.postimg.cc/YqGbvB4C/Screenshot-2023-08-20-112910.png)](https://postimg.cc/JG8bFgcf)
[![Screenshot-2023-08-20-112920.png](https://i.postimg.cc/VsHKskkh/Screenshot-2023-08-20-112920.png)](https://postimg.cc/pyzfqx8Q)

* **Buy**: Buy a stock. Must input a stock ticker and amount of shares to buy. Error message is presented if the stock ticker is invalid, the number of shares is not a positive integer, or if there are insufficient funds to purchase stock.

_Buy Stock Form_

[![Screenshot-2023-08-20-112932.png](https://i.postimg.cc/bJymrGn7/Screenshot-2023-08-20-112932.png)](https://postimg.cc/zLQCPG07)

_Error Message_

[![Screenshot-2023-08-20-113001.png](https://i.postimg.cc/zv3pw90p/Screenshot-2023-08-20-113001.png)](https://postimg.cc/p5bDR1Nn)

* **Sell**: Sell a stock. Shows a dropdown of all currently owned stocks and a form to input the number of shares to sell. Error message is presented if the number of shares to sell is more than currently owned or if the number is not a positive integer.

_Sell Stock Form_

[![Screenshot-2023-08-20-113018.png](https://i.postimg.cc/wMP2w0rz/Screenshot-2023-08-20-113018.png)](https://postimg.cc/7J3S6MDt)

_Error Message_

[![Screenshot-2023-08-20-113038.png](https://i.postimg.cc/W469smdm/Screenshot-2023-08-20-113038.png)](https://postimg.cc/Z9nPcdF0)

* **Trade History**: View trade history of buying/selling stocks. Shows each trade and its order type (buy/sell), stock symbol, number of shares, order price, total value bought/sold, and time the trade occurred.

[![Screenshot-2023-08-20-113052.png](https://i.postimg.cc/Xv381Zsr/Screenshot-2023-08-20-113052.png)](https://postimg.cc/tsSWYgQb)

* **Deposit**: Deposit cash. Input amount of cash in USD to deposit. Error message is presented if the amount of cash that the user wishes to deposit is less than 0.
  
[![Screenshot-2023-08-20-113059.png](https://i.postimg.cc/hj2pdSbf/Screenshot-2023-08-20-113059.png)](https://postimg.cc/G8sF0nfC)

* **Logout**: Logs users out of their account and redirects to the login page. This automatically occurs if the user is not logged in already and tries to access any page other than register, login, or logout. 

## Clone Repository & API Keys

To access the project, clone the repository and then get a TwelveData API KEY to get stock data at https://twelvedata.com/. Also make your own random SECRET KEY for configuring Flask Session. Python, Flask, and multiple libraries must also be installed on your computer. 

[![Screenshot-2023-08-20-115208.png](https://i.postimg.cc/zDFk2mvx/Screenshot-2023-08-20-115208.png)](https://postimg.cc/mhhMh5Q9)

## SQL Database Structure 

[![Screenshot-2023-08-20-115435.png](https://i.postimg.cc/pT6PRcX4/Screenshot-2023-08-20-115435.png)](https://postimg.cc/0MDTCfS0)

## Security 

Password hashing with Werkzeug Security is used before storing passwords in the SQL Database. 

## Project Filesystem

[![Screenshot-2023-08-20-115358.png](https://i.postimg.cc/C11FypYb/Screenshot-2023-08-20-115358.png)](https://postimg.cc/yJMq95DN)

## Author & Credits

Created by William Pan. 

