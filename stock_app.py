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
        self.frames = {}
        for F in (StartPage, BTCe_page, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
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
        button3 = ttk.Button(self, text="Take Backup to flat file", command=controller.sql_interface.backup)
        button3.pack()
        button4 = ttk.Button(self, text="Restore Backup from flat file", command=controller.sql_interface.restore)
        button4.pack()

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
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class SQLinterface():
    sql_link = 'sqlite:///market.db'
    records_dict = {}
    
    def __init__(self):
        try:
            self.engine = create_engine(self.sql_link, echo = True)
        except Operation:
            self.meta = MetaData()
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
            
    
    def retreive_data(self):
        list_of_stocks = self.session.query(Stock).filter(Stock.symbol.in_(['IRCTC'])).all()
        df = pd.DataFrame()
        for stock in list_of_stocks:
            df.append(stock.to_df())
        return df
    
    def backup(self):
        query = "SELECT * FROM STOCKS"
        df = pd.read_sql(query, con=self.engine)
        df.to_csv("Backup.csv")
        
    def restore(self):
        df = pd.read_csv("Backup.csv")
        df.to_sql(name=Stock.__tablename__, con=self.engine, index=False)
        
    def check_database(self):
        
 
class Stock(Base):
    __tablename__ = 'stocks'
    
    symbol = Column('Symbol', String, primary_key=True)
    date = Column('Date', Integer, primary_key=True)
    prev_close = Column('Prev Close', Float)
    open_price = Column('Open Price', Float)
    high_price = Column('High Price', Float)
    low_price = Column('Low Price', Float)
    last_price = Column('Last Price', Float)
    close_price = Column('Close Price', Float)
    average_price = Column('Average Price', Float)
    total_traded_quantity = Column('Total Traded Quantity', BigInteger)
    turnover = Column('Turnover', Float)
    no_of_trades = Column('No. Of Trades', Integer)
    delivery_qty = Column('Deliverable Qty', BigInteger)
    percent_dly_qt2trading_qty = Column('% Dly Qt to Traded Qty', Float)
    
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

app = SeaofBTCapp()
app.mainloop()