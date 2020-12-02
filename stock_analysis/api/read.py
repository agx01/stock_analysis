# -*- coding: utf-8 -*-
import urllib3
import json
import os
import pandas as pd

class StockRead():
    
    def __init__(self):
        __config_file__ = "config.json"
        config_file_path = "C:\\"+os.path.join("Users", "Arijit Ganguly", "Documents", "PythonProjects", "stock_analysis", "stock_analysis", __config_file__)
        with open(config_file_path, 'r') as json_file:
            data = json.load(json_file)
            self.stock_read_link = data["Links"]["stocks"]["Read"]
            self.stock_read_by_symbol = data["Links"]["stocks"]["Search by Symbol"]
            self.unique_stocks = data["Links"]["stocks"]["Unique Stocks"]
            self.data_path = data["Project Structure"]["Data"]
            self.historic_data_path = data["Project Structure"]["Historic stocks"]
        
    def read_all(self):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET', 
                             self.stock_read_link, 
                             headers={'Content-Type':'application/json',
                                      'Accept':'*/*',
                                      'Accept-Encoding':'gzip,deflate,br',
                                      'Connection':'keep-alive',
                                      'User-Agent':'Python-Frontend'})
            json_dump = json.loads(r.data)
            df = pd.json_normalize(json_dump['records'])
            return df
        except urllib3.exceptions.NewConnectionError as e:
            print("Error: "+str(e))       
            return None
        
    def get_unique_stocks(self):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET',
                             self.unique_stocks,
                             headers={'Content-Type':'application/json',
                                      'Accept':'*/*',
                                      'Accept-Encoding':'gzip,deflate,br',
                                      'Connection':'keep-alive',
                                      'User-Agent':'Python-Frontend'})
            json_dump = json.loads(r.data)
            df = pd.json_normalize(json_dump['records'])
            return df
        except urllib3.exceptions.NewConnectionError as e:
            print("Error: "+str(e))
            return None
    
    def build_historic_data_structure(self):
        df = self.get_unique_stocks()
        for index, row in df.iterrows():
            target_dir = os.path.join(self.historic_data_path, row["symbol"])
            if os.path.isdir(target_dir):
                print("Folder already present")
            else:
                os.mkdir(target_dir)
                print("Folder created")
    
    def read_data_by_symbol(self, symbol):
        http = urllib3.PoolManager()
        url_link = self.stock_read_by_symbol+symbol
        try:
            r = http.request('GET',
                             url_link,
                             headers={'Cotent-Type':'application/json',
                                      'Accept':'*/*',
                                      'Accept-Encoding':'gzip,defalte,br',
                                      'Connection':'keep-alive',
                                      'User-Agent':'Python-Frontend'})
            json_dump = json.loads(r.data)
            df = pd.json_normalize(json_dump['records'])
            return df
        except urllib3.exceptions.NewConnectionError as e:
            print("Error: "+str(e))
            return None