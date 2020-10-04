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
        
    def get_dates():
        http = urllib3.PoolManager()