# -*- coding: utf-8 -*-
from stock_analysis.api.extraction import StockExtraction

stock_extraction = StockExtraction()
stock_extraction.extract_daily_stock_data("02102020")
