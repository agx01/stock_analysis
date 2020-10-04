# -*- coding: utf-8 -*-

from stock_analysis.api.read import StockRead
import pandas as pd

stock_read = StockRead()
df = stock_read.read_all()
print(df)