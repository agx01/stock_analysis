# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:55:40 2020

@author: Arijit Ganguly
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Float, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from datetime import datetime
from functools import reduce

import matplotlib.pyplot as plt

import urllib3, json
import os
import shutil
from selenium import webdriver
import time

Base = declarative_base()


LARGE_FONT = ("Verdana", 12)
    
    
class SeaofBTCapp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Sea of BTC Client")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.sql_interface = SQLinterface()
        
        api = Api_Interface()
        #api.read_all("stock")
        #api.extract_daily_stock_data()
        
        self.frames = {}
        for F in (StartPage, BTCe_page, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            #if F is BTCe_page:
                #frame.after(2, self.sql_interface.retreive_data())
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
def qf(quickPrint):
    print(quickPrint)

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
        
        button2 = ttk.Button(self, text="Disagree",
                            command=parent.destroy)
        button2.pack()
       

class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Graph",
                            command=lambda: controller.show_frame(BTCe_page))
        button2.pack()
        button3 = ttk.Button(self, text="Extract Daily Load", command=api.extract_daily_stock_data)
        button3.pack()
        button4 = ttk.Button(self, text="Read all data", command=api.read_all)
        button4.pack()
        button5 = ttk.Button(self, text="Test function button", command=controller.sql_interface.drop_data)
        button5.pack()
        
class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home",
                            command= lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
class BTCe_page(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home",
                             command= lambda: controller.show_frame(StartPage))
        button1.pack()
        f = Figure(dpi=150, tight_layout=True)
        '''
        my_data = controller.sql_interface.retreive_graph1data()
        
        fig_size =(25,10)
        
        ax = [f.add_subplot(2,2,i+1) for i in range(4)]
        for a in ax:
            (my_data /my_data.iloc[0] * 100).plot(figsize=fig_size, ax=a)
            #a.set_aspect('equal')
        
        #plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        #f.subplots_adjust(wspace=0, hspace=0)
        '''
        '''
        a = f.add_subplot(221)
        a.set_aspect('equal')
        (my_data /my_data.iloc[0] * 100).plot(figsize=fig_size, ax=a)
        
        b = f.add_subplot(222)
        b.set_aspect('equal')
        (my_data /my_data.iloc[0] * 100).plot(figsize=fig_size, ax=b);
        
        c = f.add_subplot(223)
        c.set_aspect('equal')
        (my_data /my_data.iloc[0] * 100).plot(figsize=fig_size, ax=c);
        
        d = f.add_subplot(224)
        d.set_aspect('equal')
        (my_data /my_data.iloc[0] * 100).plot(figsize=fig_size, ax=d);
        
        #f.subplots_adjust(wspace=0, hspace=0)
        '''
        #plt.show()
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class SQLinterface():
    sql_link = 'sqlite:///market.db'
    records_dict = {}
    meta = MetaData()
    
    def __init__(self):
        self.engine = create_engine(self.sql_link, echo = True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        #self.get_no_of_records()
    
    def get_no_of_records(self):
        total_sql_records_query = "SELECT COUNT(*) FROM STOCKS"
        df = pd.read_sql(total_sql_records_query, con=self.engine)
        self.total_records = int(df.iloc[0,0])
        print(self.total_records)
        stocks_query = "SELECT DISTINCT(Symbol) FROM STOCKS"
        stocks_df =  pd.read_sql(stocks_query, con=self.engine)
        self.stocks = stocks_df.iloc[0].to_list()
        print(self.stocks)
        for stock in self.stocks:
            records_query = "SELECT COUNT(*) FROM STOCKS WHERE Symbol='"+stock+"'"
            df = pd.read_sql(records_query, con=self.engine)
            self.records_dict[stock] = int(df.iloc[0,0])
        print(self.records_dict)
            
    def revert_dates(self, x):
        str_date = str(x)
        date_dict = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10': 'Oct', '11':'Nov', '12':'Dec'}
        str0 = str_date[:4]
        str1 = str_date[4:6]
        str2 = str_date[6:]
        str1 = date_dict[str1]
        return str2+'-'+str1+'-'+str0
    '''
    def retreive_graph1data(self):
        all_frames = {}
        query = "SELECT DISTINCT Symbol FROM Stocks"
        stock_list_df = pd.read_sql(query, con=self.engine)
        query = "SELECT DISTINCT Symbol FROM Indices"
        indices_list_df = pd.read_sql(query, con=self.engine)
        for index,row in indices_list_df.iterrows():
            query = "SELECT Date,Close FROM INDICES WHERE SYMBOL='"+row[0]+"'"
            df1 = pd.read_sql(query, con=self.engine)
            df1 = df1.rename({'CLOSE':row[0]}, axis='columns')
            df1 = df1.sort_values('DATE', ascending=True)
            all_frames[row[0]] = df1
        
        data_frames = []
        for key in all_frames.keys():
            data_frames.append(all_frames[key])
            
        my_data = reduce(lambda left,right: pd.merge(left, right, on=['DATE'], how='outer'), data_frames).fillna(0)
        my_data['DATE'] = my_data['DATE'].apply(lambda x: self.revert_dates(x))
        my_data = my_data.set_index('DATE')
        return my_data
     '''              
    def backup(self):
        date_today = date.today().isoformat()
        query = "SELECT * FROM STOCKS"
        df = pd.read_sql(query, con=self.engine)
        df.to_csv("Backup_stocks_"+date_today+".csv")
        query = "SELECT * FROM INDICES"
        df = pd.read_sql(query, con=self.engine)
        df.to_csv("Backup_indices_"+date_today+".csv")
        
    def restore(self):
        stock_columns_mapping = {'Symbol':'SYMBOL', 'Date':'DATE', 'Prev Close': 'PREVCLOSE', 'Open Price': 'OPEN', 'High Price':'HIGH', 'Low Price': 'LOW', 'Last Price': 'LAST', 'Close Price':'CLOSE', 'Average Price': 'AVERAGE', 'Total Traded Quantity':'TOTALTRADEQTY', 'Turnover':'TURNOVER', 'No. of Trades':'TRADECOUNT', 'Deliverable Qty':'DELIVERABLEQTY', '% Dly Qt to Traded Qty':'PDLYQTY2TRADEQTY'}
        index_columns_mapping = {'Index':'INDEX', 'Date': 'DATE', 'Open':'OPEN', 'High':'HIGH', 'Low':'LOW', 'Close':'CLOSE', 'Shares Traded': 'SHARESTRADE', 'Turnover':'TURNOVER'}
        df = pd.read_csv("Backup.csv")
        df = df.rename(columns = stock_columns_mapping)
        df.to_sql(name=Stock.__tablename__, con=self.engine, index=False)
        df = pd.read_csv("Backup_index.csv")
        df = df.rename(columns = index_columns_mapping)
        df.to_sql(name=Indices.__tablename__,con=self.engine, index=False)
        self.check_database()
    
    def drop_data(self):
        query = "DROP TABLE IF EXISTS stocks"
        result = self.engine.execute(query)
        query = "DROP TABLE IF EXISTS indices"
        result =self.engine.execute(query)
        
    def check_database(self):
        query = "SELECT * FROM stocks"
        df = pd.read_sql(query, con =self.engine)
        print(df.head(5))
        query = "SELECT * FROM indices"
        df = pd.read_sql(query, con =self.engine)
        print(df.head(5))

class Stock(Base):
    
    __tablename__ = 'stocks'
    
    symbol = Column('Symbol', String, primary_key=True)
    date = Column('Date', Integer, primary_key=True)
    prev_close = Column('PrevClose', Float)
    open_price = Column('Open', Float)
    high_price = Column('High', Float)
    low_price = Column('Low', Float)
    last_price = Column('Last', Float)
    close_price = Column('Close', Float)
    average_price = Column('Average', Float)
    total_traded_quantity = Column('TotalTradeQty', BigInteger)
    turnover = Column('Turnover', Float)
    no_of_trades = Column('TradeCount', Integer)
    delivery_qty = Column('DeliverableQty', BigInteger)
    percent_dly_qt2trading_qty = Column('PDLYQTY2TRADEQTY', Float)
    
    def __repr__(self):
        return "Stock(symbol='%s', \
                date='%s', prev_close='%s', \
                open_price='%s',\
                high_price='%s',\
                low_price='%s',\
                last_price='%s',\
                close_price='%s',\
                average_price='%s',\
                total_traded_qty='%s',\
                turnover='%s',\
                no_of_trades='%s',\
                delivery_qty='%s',\
                oercent_dly_qt2trading_qty)" % \
                (self.symbol,\
                 self.date,\
                 self.open_price,\
                 self.high_price,\
                 self.low_price,\
                 self.last_price,\
                 self.close_price,\
                 self.average_price,\
                 self.total_traded_quantity,\
                 self.turnover,\
                 self.no_of_trades,\
                 self.delivery_qty,\
                 self.percent_dly_qt2trading_qty)
                    
    def to_dict(self):
        return {'symbol':self.symbol,
                'date':self.date,
                'open_price':self.open_price,
                'high_price':self.high_price,
                'low_price':self.low_price,
                'last_price':self.last_price,
                'close_price':self.close_price,
                'average_price':self.average_price,
                'total_traded_quantity':self.total_traded_quantity,
                'turnover':self.turnover,
                'no_of_trades':self.no_of_trades,
                'delivery_qty':self.delivery_qty,
                'percent_dly_qt2trading_qt':self.percent_dly_qt2trading_qty}
    
    def to_df(self):
        return pd.DataFrame.from_dict(self.to_dict(), orient='index')
    
class Indices(Base):
    __tablename__ = "indices"
    
    index = Column('Index', String, primary_key=True)
    date = Column('Date', Integer, primary_key=True)
    open_price = Column('Open', Float)
    high_price = Column('High', Float)
    low_price = Column('Low', Float)
    close_price = Column('Close', Float)
    shares_traded = Column('SharesTraded', Float)
    turnover = Column('Turnover', Float)
    
    def __repr__(self):
        return "Stock(symbol='%s', \
                date='%s', prev_close='%s', \
                open_price='%s',\
                high_price='%s',\
                low_price='%s',\
                close_price='%s',\
                shares_traded='%s',\
                turnover='%s',\)" % \
                (self.symbol,\
                 self.date,\
                 self.open_price,\
                 self.high_price,\
                 self.low_price,\
                 self.close_price,\
                 self.shares_traded,\
                 self.turnover)
    
    def to_df(self):
        return pd.DataFrame.from_dict(self.to_dict(), orient='index')

class Tradebook():
    __tablename__ = "tradebook"
    
    date = Column('Date', Integer)
    symbol = Column('Symbol', String)
    exchange = Column('Exchange', String)
    segment = Column('Segment', String)
    trade_type = Column('TradeType', String)
    quantity = Column('Quantity', String)
    price = Column('Price', String)
    order_id = Column('OrderID', String)
    trade_id = Column('TradeID', String, primary_key=True)
    exec_time = Column('Execution_time', String)
    
    def __repr__(self):
         return "Stock(date='%s', \
                symbol='%s', \
                exchange='%s', \
                segment='%s',\
                trade_type='%s',\
                quantity='%s',\
                close_price='%s',\
                shares_traded='%s',\
                turnover='%s',\)" % \
                (self.date,\
                 self.symbol,\
                 self.exchange,\
                 self.segment,\
                 self.trade_type,\
                 self.close_price,\
                 self.shares_traded,\
                 self.turnover)
    
class Portfolio():
    __tablename__ = "portfolio"
    stock = ()
    
    def __init__(self):
        pass


class Api_Interface():
    base_nse_url = "https://archives.nseindia.com/products/content/"
    http = urllib3.PoolManager()
    home_url = "http://www.arijitganguly.com/api/"
    data_map = {"index": "/indices/", "stock":"/stock/"}
    functions_map = {"read": "read.php", "search":"search.php", "create":"create.php"}
    
    def __init__(self):
        pass
    
    def extract_bhavcopy_from_nse(self, file_name):
        url = self.base_nse_url+file_name
        driver = webdriver.Chrome('C:\Work\chromedriver_win32\chromedriver')
        try:
            driver.get(url)
            time.sleep(2)
            print("File Downloaded")
        except Exception as e:
            print(e.message)
            print("File download not successful")
        
    
    def read_all(self, data_required):
        try:
            response = self.http.request('GET',self.home_url+self.data_map[data_required]+self.functions_map["read"])
            data = json.loads(response.data.decode('utf-8'))
            df = pd.json_normalize(data["records"])
            print(df)
        except urllib3.exceptions.NewConnectionError as e:
            print(e.message)
    
    def get_date_for_extraction(self):
        today = date.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%d&m&Y")
        return yesterday
        
    def get_bhavdata_file(self):
        download_path = "C:\\"+os.path.join("Users","Arijit Ganguly","Downloads")
        yesterday = self.get_date_for_extraction()
        target_path = os.path.join(os.getcwd(), "Data")
        #check if a folder exists with yesterday's date in Data folder
        if os.path.isdir(os.path.join(target_path, yesterday)):
            print("Folder already exists")
            shutil.move(os.path.join(download_path,file_name), os.path.join(target_path,date,file_name))
        else:
            print("Creating folder")
            os.mkdir(os.path.join(target_path,date))
            shutil.move(os.path.join(download_path,file_name), os.path.join(target_path,date,file_name))
            print("Bhavdata file copied from the dowloads folder")
            
        
    
    def create_one(self, data_required, json_record):
        try:
            r = self.http.request('POST', self.home_url+self.data_map[data_required]+self.functions_map["create"], headers={'Content-Type':'application/json', 'Accept':'*/*', 'Accept-Encoding':'gzip,deflate,br', 'Connection':'keep-alive', 'User-Agent':'Python-Frontend'}, body=json_record)
            print(r.status)
            print(r.data)
            r.release_conn()
        except urllib3.exceptions.NewConnectionError as e:
            print(e.message)
    
    def change_date(self, date):
        year = date[7:]
        month = date[3:6]
        day = date[:2]
        month_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        return year+'-'+month_dict[month]+'-'+day

    def transform_dataframe(self,df):
        dataframe = pd.DataFrame()
        dataframe = df
        
        #Rename the columns as per the json to be created
        dataframe = dataframe.rename(columns={"SYMBOL":"symbol",
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
        
        #Replace the hyphens in the csv with 0 value
        dataframe.deliv_qty = dataframe.deliv_qty.replace({" -":0})
        dataframe.deliv_per = dataframe.deliv_per.replace({" -":0})
        dataframe.last_price = dataframe.last_price.replace({" ":0})
        
        #typecast the data as is required in the table
        dataframe["deliv_qty"] = dataframe["deliv_qty"].astype(int)
        dataframe["deliv_per"] = dataframe["deliv_per"].astype(float)
        dataframe["last_price"] = dataframe["last_price"].astype(float)
        
        #remove excess spaces in the data
        dataframe["series"] = dataframe["series"].str.strip()
        dataframe["trading_date"] = dataframe["trading_date"].str.strip()
        
        #transform the date format to the SQL format
        dataframe["trading_date"] = dataframe["trading_date"].apply(lambda x : self.change_date(x))
        return dataframe
    
    def extract_daily_stock_data(self):
        yesterday = self.get_date_for_extraction()
        file_name = "sec_bhavdata_full_"+yesterday+".csv"
        self.extract_bhavcopy_from_nse(file_name)
        self.get_bhavdata_file()
        file_name = "sec_bhavdata_full_"+yesterday+".csv"
        file = os.path.join(os.getcwd(),"Data", yesterday,file_name)
        df = pd.read_csv(file).fillna(0)
        df = self.transform_dataframe(df)
        for index,row in df.iterrows():
            #creating a custom dictionary
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
            
            #creating a json dump using dictionary
            json_dump = json.dumps(data).encode()
            
            #create a record in the SQL table for this row in dataframe
            self.create_one("stock",json_dump)
                 
        
app = SeaofBTCapp()
app.mainloop()