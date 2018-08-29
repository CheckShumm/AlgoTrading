# import libraries

import pandas as pd

import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


from iexfinance import Stock
from iexfinance import get_historical_data

# plotting style
style.use('ggplot')

# data timeline
start = dt.datetime(2015, 12, 22)
end = dt.datetime(2017, 5, 24)

df = get_historical_data('TSLA', start=start, end=end, output_format='pandas')

df.index = pd.to_datetime(df.index)

print(df.head())

df_ohlc = df['close'].resample('10D').ohlc()
df_volume = df['volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

#df['100ma'] = df['close'].rolling(window=100).mean()

df.dropna(inplace=True)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()
