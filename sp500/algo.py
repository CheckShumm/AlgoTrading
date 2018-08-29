

import os
import datetime as dt
import pandas as pd

import pickle
import requests
import bs4 as bs

import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


from iexfinance import Stock
from iexfinance import get_historical_data

# grab S&P 500 company titles
def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class' : 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers

# store data locally
def get_iex_stock_data(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2015, 12, 22)
    end = dt.datetime(2017, 5, 24)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = get_historical_data(ticker, start=start, end=end, output_format='pandas')
            df.index = pd.to_datetime(df.index)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already stored {}'.format(ticker))

def compile_data():
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('date', inplace=True)

        df.rename(columns = {'close' : ticker}, inplace=True)
        df.drop(['open', 'high','low', 'volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

compile_data()
