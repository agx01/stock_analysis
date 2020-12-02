# -*- coding: utf-8 -*-

from stock_analysis.api.read import StockRead
from sklearn import preprocessing
import numpy as np

stock_read = StockRead()
df = stock_read.read_data_by_symbol('RELIANCE')
df = df[df['series'] == "EQ"]
df = df.sort_values(by=['trading_date'])
history_points = 50

data = df.drop(['symbol', 'trading_date', 'series', 'last_price', 'avg_price', 'deliv_per', 'deliv_qty', 'prev_close', 'turnover_lacs', 'no_of_trades'], axis=1)
data['open'] = data['open'].astype(float)
data['high'] = data['high'].astype(float)
data['low'] = data['low'].astype(float)
data['close'] = data['close'].astype(float)
data['ttl_trd_qnty'] = data['ttl_trd_qnty'].astype(float)
data_normaliser = preprocessing.MinMaxScaler()
data_normalised = data_normaliser.fit_transform(data)

ohlcv_histories_normalised = np.array([data_normalised[i : i + history_points].copy() for i in range(len(data_normalised) - history_points)])
next_day_open_values_normalised = np.array([data_normalised[:,0][i + history_points].copy() for i in range(len(data_normalised) - history_points)])
next_day_open_values_normalised = np.expand_dims(next_day_open_values_normalised, -1)

next_day_open_values = np.array([data.iloc[:,0][i + history_points].copy() for i in range(len(data) - history_points)])
next_day_open_values = np.expand_dims(next_day_open_values_normalised, axis=1)

y_normaliser = preprocessing.MinMaxScaler()
y_normaliser.fit(np.expand_dims( next_day_open_values, axis=1 ))

'''
def normalised_data():
    stock_read = StockRead()
    df = stock_read.read_data_by_symbol('RELIANCE')
    df = df[df['series'] == "EQ"]
    df = df/sort_values(by=['trading_date'])
    history_points = 50
    data = df.drop(['symbol', 'trading_date', 'series', 'last_price', 'avg_price', 'deliv_per', 'deliv_qty', 'prev_close', 'turnover_lacs', 'no_of_trades'], axis=1)
    data_normaliser = preprocessing.MinMaxScaler()
    data_normalised = data_normaliser.fit_transform(data)
    
    ohlcv_histories_normalised = np.array([data_normarlised[i : i + history_points].copy() for i in range(len(data_normalised)-history_points)])
'''  