# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 18:19:05 2020

@author: Arijit Ganguly
"""

import requests
from requests.exceptions import HTTPError
import urllib3, json
import pandas as pd
import time
import os
from selenium import webdriver

chromedriver = "C:\\"+os.path.join("Work","chromedriver_win32", "chromedriver")

def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text
    
def convert_hyphen(text):
    if text == " -":
        return 0
    else:
        return text
'''
def change_date(date):
    year = date[7:]
    month = date[3:6]
    day = date[:2]
    month_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    return year+'-'+month_dict[month]+'-'+day
    

http = urllib3.PoolManager()

url2 = "http://www.arijitganguly.com/api/stock/create.php"
df2 = pd.read_csv('sec_bhavdata_full(1).csv').fillna(0)

df2 = df2.rename(columns={"SYMBOL":"symbol",
                          " SERIES":"series",
                          " DATE1":"trading_date",
                          " PREV_CLOSE":"prev_close",
                          " OPEN_PRICE":"open",
                          " HIGH_PRICE":"high",
                          " LOW_PRICE":"low",
                          " LAST_PRICE":"last_price",
                          " CLOSE_PRICE":"close",
                          " AVG_PRICE":"avg_price",
                          " TTL_TRD_QNTY":"ttl_trd_qnty",
                          " TURNOVER_LACS":"turnover_lacs",
                          " NO_OF_TRADES":"no_of_trades",
                          " DELIV_QTY":"deliv_qty",
                          " DELIV_PER":"deliv_per"}, errors="raise")
df2.deliv_qty = df2.deliv_qty.replace({" -":0})
df2.deliv_per = df2.deliv_per.replace({" -":0})
df2.last_price = df2.last_price.replace({" ":0})
df2["deliv_qty"] = df2["deliv_qty"].astype(int)
df2["deliv_per"] = df2["deliv_per"].astype(float)
df2["last_price"] = df2["last_price"].astype(float)
df2["series"] = df2["series"].str.strip()
df2["trading_date"] = df2["trading_date"].str.strip()
#df2["deliv_qty"] = df2["deliv_qty"].str.strip()
#df2["deliv_per"] = df2["deliv_per"].str.strip()
df2["trading_date"] = df2["trading_date"].apply(lambda x : change_date(x))


#json_dump = json.dumps(data)
#print(json_dump)
#data_dict = data.to_dict('r')
#data_dict_json = json.dump(data_dict)s
'''
'''
headers = {'content-type': 'application/json'}
response = requests.post(url2, data=json.dumps(data), headers=headers)
print(response.read().decode('utf-8'))
'''
'''
'''
'''
try:
    req = urllib3.request.Request(url2)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Content-Length', len(json_dump))
    req.add_header('Accept', 'text/plain')
    response = urllib3.request.urlopen(req, json_dump)
    print(response.read().decode('utf-8'))
    
except urllib.error.HTTPError as e:
    body = e.read().decode()

_json = json.loads(body)
print(body)
'''
'''
for index, row in df2.iterrows():
    data = {}
    data["symbol"] = row["symbol"]
    data["trading_date"] = row["trading_date"]
    data["prev_close"] = row["prev_close"]
    data["open"] = row["open"]
    data["high"] = row["high"]
    data["low"] = row["low"]
    data["close"] = row["close"]
    data["last_price"] = row["last_price"]
    data["avg_price"] = row["avg_price"]
    data["ttl_trd_qnty"] = row["ttl_trd_qnty"]
    data["turnover_lacs"] = row["turnover_lacs"]
    data["no_of_trades"] = row["no_of_trades"]
    data["deliv_qty"] = row["deliv_qty"]
    data["deliv_per"] = row["deliv_per"]
    data["series"] = row["series"]
    print(data)
    
    json_dump = json.dumps(data).encode()
    
    try:
        print(json_dump)
        r = http.request('POST', url2, headers={'Content-Type':'application/json', 'Accept':'*/*', 'Accept-Encoding':'gzip,deflate,br', 'Connection':'keep-alive', 'User-Agent':'Python-Frontend'}, body=json_dump)
        print(r.status)
        print(r.data)
    except urllib3.exceptions.NewConnectionError as e:
        print(e.message)
    

url = "http://www.arijitganguly.com/api/stock/read.php"
response = http.request('GET', url)
data = json.loads(response.data.decode('utf-8'))
df = pd.json_normalize(data["records"])
print(df)
'''
'''
url3 = "https://archives.nseindia.com/products/content/sec_bhavdata_full_18092020.csv"

from selenium import webdriver
from datetime import date
import shutil
today = date.today()
date = today.strftime("%d%m%Y")
date = "18092020"
file_name = "sec_bhavdata_full_"+date+".csv"
base_url = "https://archives.nseindia.com/products/content/"
download_path = "C:\\"+os.path.join("Users","Arijit Ganguly","Downloads")
target_path = os.path.join(os.getcwd(),"Data")
print(base_url+file_name)

driver = webdriver.Chrome('C:\Work\chromedriver_win32\chromedriver')

driver.get(base_url+file_name)
time.sleep(2)

def create_folder(date, file_name, target_path):
    if os.path.isdir(os.path.join(target_path,date)):
        print("folder already present")
        shutil.move(os.path.join(download_path,file_name), os.path.join(target_path,date,file_name))
    else:
        print("Creating folder")
        os.mkdir(os.path.join(target_path,date))
        shutil.move(os.path.join(download_path,file_name), os.path.join(target_path,date,file_name))

create_folder("18092020", file_name, target_path)
'''
'''
def change_date(str_date):
        """
        Function to change date format from DDMMYYYY to YYYY-MM-DD

        Parameters
        ----------
        date : String
            Date format DDMMYYYY which is bhavcopy format

        Returns
        -------
        String
            Date in the format YYYY-MM-DD which is in the SQL table format

        """
        year = str_date[6:]
        month = str_date[3:5]
        day = str_date[:2]
        return year+'-'+month+'-'+day
file = "C:\\"+os.path.join("Users", "Arijit Ganguly", "Downloads", "ind_close_all_09102020.csv")
dataframe = pd.read_csv(file).fillna(0)
dataframe = dataframe.rename(columns={"Index Name":"index_name",
                                              "Index Date":"trading_date",
                                              "Open Index Value":"open",
                                              "High Index Value":"high",
                                              "Low Index Value":"low",
                                              "Closing Index Value":"close",
                                              "Points Change":"pts_change",
                                              "Change(%)":"change_percent",
                                              "Volume":"volume",
                                              "Turnover (Rs. Cr.)":"turnover",
                                              "P/E":"p_by_e",
                                              "P/B":"p_by_b",
                                              "Div Yield":"div_yield"})
dataframe.open = dataframe.open.replace({"-":0})
dataframe.high = dataframe.high.replace({"-":0})
#dataframe.close = dataframe.close.replace({"-":0})
dataframe.low = dataframe.low.replace({"-":0})
#dataframe.pts_change = dataframe.pts_change.replace({"-":0})
dataframe.change_percent = dataframe.change_percent.replace({"-":0})
dataframe.volume = dataframe.volume.replace({"-":0})
dataframe.turnover = dataframe.turnover.replace({"-":0})
dataframe.p_by_e = dataframe.p_by_e.replace({"-":0})
dataframe.p_by_b = dataframe.p_by_b.replace({"-":0})
dataframe.div_yield = dataframe.div_yield.replace({"-":0})
dataframe["trading_date"] = dataframe["trading_date"].apply(lambda x: change_date(x))
dataframe["open"] = dataframe["open"].astype(float)
dataframe["high"] = dataframe["high"].astype(float)
dataframe["low"] = dataframe["low"].astype(float)
dataframe["close"] = dataframe["close"].astype(float)
dataframe["change_percent"] = dataframe["change_percent"].astype(float)
dataframe["volume"] = dataframe["volume"].astype('int64')
dataframe["turnover"] = dataframe["turnover"].astype(float)
dataframe["p_by_e"] = dataframe["p_by_e"].astype(float)
dataframe["p_by_b"] = dataframe["p_by_b"].astype(float)
dataframe["div_yield"] = dataframe["div_yield"].astype(float)
'''
url = "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm"
driver = webdriver.Chrome(chromedriver)
driver.get(url)
inputElement = driver.find_element_by_id("symbol")
inputElement.send_keys('RELIANCE')
radioButton = driver.find_element_by_id("rdDateToDate")
radioButton.click()
fromDate = driver.find_element_by_id("fromDate")
fromDate.send_keys("28-09-2020")
toDate = driver.find_element_by_id("toDate")
toDate.send_keys("28-09-2020")
getButton = driver.find_element_by_id("submitMe")
getButton.click()