# python_tradingview_data_wrapper
Retrieves real-time data from any Tradingview symbol and returns a Python dictionary with information on all technical indicators

## Install

Download the **TVwrapper.py** file and save it to your Python project directory

## How to work

***Import TVwrapper***

`from TVwrapper import *`


***Use the Tv class.
You can use only the "market" parameter for some functions.***


`btc = Tv(market='crypto')`


***And get all the exchanges in the market in a list using the following function***


`print(btc.get_exchanges())`


***If you want to get all the symbols of an exchange, use the following function adding the exchange of interest to the Tv class.***

```
btc = Tv(market='crypto', exchange='binance)
print(btc.get_symbols_exchange())
```


***To get all technical analysis data and indicators for a symbol you should use the following function:***

```
btc = Tv(symbol='BTCUSDT', market='crypto', exchange='binance)
print(btc.get_indicators())
```

It will return you a real-time dictionary of the value of all indicators.

The indicators will appear as follows:

_rsi_0 (Current Candlestick)_

_rsi_1 (Previous candlestick)_

_rsi_2 (Candle previous to rsi_1)_

_rsi_3 (Candle previous to rsi_2)_


So you can work with up to 3 candles prior to the current candle with any technical indicator.
