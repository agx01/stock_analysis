# -*- coding: utf-8 -*-
from stock_analysis.api.extraction import StockExtraction
from stock_analysis.api.extraction import IndexExtraction
from stock_analysis.api.read import StockRead

date = "06112020"

stock_extraction = StockExtraction()
stock_extraction.extract_daily_stock_data()
index_extraction = IndexExtraction()
index_extraction.extract_daily_index_data()
stock_read = StockRead()
stock_read.build_historic_data_structure()