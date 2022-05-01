# Tradingview data wrapper (tradingview-dw)
# Author: GaboBegue (https://github.com/GaboBegue)
# License: MIT

import requests

version = "1.0"

''' 
---Markets in TradingView---

stock_markets = ['america', 'argentina', 'australia', 'bahrain', 'belgium', 'brazil', 'canada', 'chile', 'china', 
'colombia', 'denmark', 'egypt', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'iceland', 'india', 
'indonesia', 'israel', 'italy', 'japan', 'lithuania', 'luxembourg', 'malaysia', 'mexico', 'netherlands', 
'newzealand', 'nigeria', 'norway', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 
'serbia', 'singapore', 'slovakia', 'spain', 'sweden', 'switzerland', 'thailand', 'turkey', 'uae', 'uk'] 

currencies = ['forex']
cryptocurrencies = ['crypto']
cfd = ['cfd']
'''


class Tv:
    symbol = ''
    exchange = ''
    market = ''
    interval = ''
    interv = {'1m': '|1', '5m': '|5', '15m': '|15', '1h': '|60', '2h': '|120', '4h': '|240', '1d': '', '1w': '|1W',
              '1M': '|1M'}
    tv_url = "https://scanner.tradingview.com/"
    indicators = ["RSI", "Stoch.K", "Stoch.D", "CCI20", "ADX", "ADX+DI", "ADX-DI", "AO", "Mom", "MACD.macd",
                  "MACD.signal", "Rec.Stoch.RSI", "Stoch.RSI.K", "Rec.WR", "W.R", "Rec.BBPower", "BBPower",
                  "Rec.UO", "UO", "close", "EMA5", "SMA5", "EMA10", "SMA10", "EMA20", "SMA20", "EMA30", "SMA30",
                  "EMA50", "SMA50", "EMA100", "SMA100", "EMA200", "SMA200", "Rec.Ichimoku", "Ichimoku.BLine",
                  "Rec.VWMA", "VWMA", "Rec.HullMA9", "HullMA9", "Pivot.M.Classic.S3", "Pivot.M.Classic.S2",
                  "Pivot.M.Classic.S1", "Pivot.M.Classic.Middle", "Pivot.M.Classic.R1", "Pivot.M.Classic.R2",
                  "Pivot.M.Classic.R3", "Pivot.M.Fibonacci.S3", "Pivot.M.Fibonacci.S2", "Pivot.M.Fibonacci.S1",
                  "Pivot.M.Fibonacci.Middle", "Pivot.M.Fibonacci.R1", "Pivot.M.Fibonacci.R2",
                  "Pivot.M.Fibonacci.R3", "Pivot.M.Camarilla.S3", "Pivot.M.Camarilla.S2", "Pivot.M.Camarilla.S1",
                  "Pivot.M.Camarilla.Middle", "Pivot.M.Camarilla.R1", "Pivot.M.Camarilla.R2",
                  "Pivot.M.Camarilla.R3", "Pivot.M.Woodie.S3", "Pivot.M.Woodie.S2", "Pivot.M.Woodie.S1",
                  "Pivot.M.Woodie.Middle", "Pivot.M.Woodie.R1", "Pivot.M.Woodie.R2", "Pivot.M.Woodie.R3",
                  "Pivot.M.Demark.S1", "Pivot.M.Demark.Middle", "Pivot.M.Demark.R1", "open", "P.SAR", "BB.lower",
                  "BB.upper", "AO", "volume", "change", "low", "high"]

    def __init__(self, symbol=symbol, exchange=exchange, market=market, interval=interval):
        self.symbol = symbol
        self.exchange = exchange
        self.market = market
        self.interval = self.itvl(interval)

    def itvl(self, interval):
        if interval in self.interv.keys():
            return self.interv[interval]
        else:
            print('If interval is empty, return interval 1 day')
            return self.interv['1d']

    def get_indicators(self):
        json_data = {'symbols': {'tickers': [f'{self.exchange.upper()}:{self.symbol.upper()}'], 'query': {'types': []}},
                     'columns': [f'{i}[{str(j)}]{self.interval}' for i in self.indicators for j in range(0, 4)]}
        if self.market == '':
            raise Exception(f'Fatal error: review and write market')
        else:
            url_req = f'{self.tv_url}{self.market.lower()}/scan'
            headers = {'User-Agent': f'tradingview_data_wrapper/{version}'}
            response = requests.post(url_req, json=json_data, headers=headers, timeout=5)
            if response.json()['data'] is not []:
                data_keys = [f'{i.lower()}_{str(j)}' for i in self.indicators for j in range(0, 4)]
                data_values = [i for i in response.json()['data'][0]['d']]
                dicc_tv = dict(zip(data_keys, data_values))
                return dicc_tv
            else:
                raise Exception(f'Data is empty: review and write correct symbol, exchange, market or interval')

    def get_exchanges(self):
        exchanges = []
        if self.market == '':
            raise Exception(f'Fatal error: review and write market')
        else:
            url_req = f'{self.tv_url}{self.market.lower()}/scan'
            response = requests.get(url_req)

            if response.json()['data'] is not []:
                for i in response.json()['data']:
                    exch = str(i['s']).find(':')
                    exchanges.append(str(i['s'])[:exch])

                return sorted(list(set(exchanges)))
            else:
                raise Exception('Error market: market not found')

    def get_symbols_exchange(self):
        symbols = []
        if self.market == '':
            raise Exception(f'Fatal error: review and write market')
        else:
            url_req = f'{self.tv_url}{self.market.lower()}/scan'
            response = requests.get(url_req)
            if response.json()['data'] is not []:
                for i in response.json()['data']:
                    symb = str(i['s']).find(':')
                    if str(i['s'])[:symb] == self.exchange.upper():
                        symbols.append(str(i['s'])[symb + 1:])

                return sorted(symbols)
            else:
                raise Exception('Error: market or exchange not found')
