# -*- coding: utf-8 -*-
import os
import json
from datetime import date
from datetime import datetime
from datetime import timedelta
import pandas as pd
import shutil
import urllib3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import logging

class StockExtraction():  
    project_structure = {}
    source_path = ""
    chrome_driver = ""
    create_one_stock = ""  
    log_path = ""
    
    def __init__(self):
        """
        Constructor function : Stock_Extraction()
        Function opens the configuration file and loads the project structure
        and links required by the functions to extract and load the data to 
        the API.
        Project Struture - Dictionary
            holds the links to internal packages and folders for use

        Returns
        -------
        None.

        """
        __config_file__ = "config.json"
        config_file_path = "C:\\"+os.path.join("Users", "Arijit Ganguly", 
                                           "Documents", "PythonProjects",
                                           "stock_analysis", "stock_analysis", 
                                           __config_file__)
        with open(config_file_path, 'r') as json_file:
            data = json.load(json_file)
            self.project_structure = data["Project Structure"]
            self.source_path = data["Project Structure"]["Download"]
            self.chrome_driver = data["Project Structure"]["Chrome driver"]
            self.create_one_stock = data["Links"]["stocks"]["Create"]
            self.nse_link = data["Links"]["Base nse url"]
            self.log_path = self.project_structure["Logs"]
        LOG_FILENAME = datetime.now().strftime(os.path.join(self.log_path, 'logfile_%H_%M_%S_%d_%m_%Y.log'))
        logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
                
    def get_date_for_extraction(self, today=date.today(), date_format="%d%m%Y"):
        """
        Function to get the latest working day date for extraction
        If today is a Monday, then it will look for Friday's date.
        If today is a Sunday, then it will look for Friday's date.
        
        Parameters
        ----------
        today : date from datetime package, optional
            This is the current date the program is run and in relation to 
            which yesterday's date can be found. 
            The default is datetime.date.today().
        date_format : String, optional
            The format in which the date needs to appear. 
            The default is "%d%m%Y".

        Returns
        -------
        yesterday : String
            Date for the last trading session is returned in 'DDMMYYYY' format
            unless specified
        """
        if today.weekday() == 0:
            delay = 3
        elif today.weekday() == 6:
            delay = 2
        else:
            delay = 1
        yesterday = today - timedelta(days=delay)
        yesterday = yesterday.strftime(date_format)
        return yesterday
    
    #Download the NSE full bhavdata copy to downloads folder
    def extract_bhavcopy_from_nse(self, file_name):
        """
        Function to download the copy of bhav copy
        It uses selenium package to work with Chrome driver to download the
        file.
        By default the file downloads in the Downlods folder

        Parameters
        ----------
        file_name : String
            The filename that is required to be extracted.

        Returns
        -------
        None.

        """
        url = self.nse_link+file_name
        driver = webdriver.Chrome(self.chrome_driver)
        try:
            driver.get(url)
            time.sleep(2)
            print("File dowload successful")
            logging.info("File download successful")
            driver.quit()
        except WebDriverException as e:
            print(str(e))
            print("File download not successful")
            logging.info("File download not successful")
            logging.debug(str(e))
  
    def change_date(self, str_date):
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
        year = str_date[7:]
        month = str_date[3:6]
        day = str_date[:2]
        month_dict = dict(Jan="01",
                          Feb="02",
                          Mar="03",
                          Apr="04",
                          May="05",
                          Jun="06",
                          Jul="07",
                          Aug="08",
                          Sep="09",
                          Oct="10",
                          Nov="11",
                          Dec="12")
        return year+'-'+month_dict[month]+'-'+day

    def transform_dataframe(self, dataframe):
        """
        Function to transform dataframe to be able to input the data in the
        SQL data
        Steps:
            1. Rename the columns
            2. Delivery quanity and Deliver per values get '-' for some stocks
                which need to be replaced with numeric value, 0.
            3. Pandas reads delivery quantity, deliver per and last price as
                string which is wrong and hence data type is changed
                Delivery quantiy : Integer
                Deliver Per : Float
                Last Price : Float
            4. String columns series and trading date has spaces for some 
                stocks which need to  be removed
            5. Date format needs to be changed to YYYY-MM-DD 
            (Month is 2 digit number)

        Parameters
        ----------
        dataframe : pandas dataframe
            Original dataframe that is based on the file from NSE website

        Returns
        -------
        dataframe : pandas dataframe
            Transformed dataframe as required by the SQL table format

        """
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
        dataframe.deliv_qty = dataframe.deliv_qty.replace({" -":0})
        dataframe.deliv_per = dataframe.deliv_per.replace({" -":0})
        dataframe["last_price"] = dataframe["last_price"].apply(lambda x: 0 if x == ' ' else x)
        dataframe["deliv_qty"] = dataframe["deliv_qty"].astype(int)
        dataframe["deliv_per"] = dataframe["deliv_per"].astype(float)
        dataframe["last_price"] = dataframe["last_price"].astype(float)
        dataframe["series"] = dataframe["series"].str.strip()
        dataframe["trading_date"] = dataframe["trading_date"].str.strip()
        dataframe["trading_date"] = dataframe["trading_date"].apply(lambda x: self.change_date(x))
        return dataframe

    def get_bhavdata_file(self, file_name, date):
        """
        Function gets the downloaded file from the Downloads folder to the
        project folder. It creates a new folder under the datasub directory 
        with the date as the name of the folder and then stores the file in it.

        Parameters
        ----------
        file_name : String
            The file name that needs to be moved to project folder
        date : String
            The date for which the extraction is accomplished. 
            Format for date is DDMMYYYY

        Returns
        -------
        None.

        """
        file_name = "sec_bhavdata_full_"+date+".csv"
        target_folder = os.path.join(self.project_structure["Data"], date)
        source_path = os.path.join(self.source_path, file_name)
        target_path = os.path.join(self.project_structure["Data"], date, file_name)
        if os.path.isdir(target_folder):
            print("Folder already exists")
            logging.info("Folder already exists")
            shutil.move(source_path, target_path)
            logging.info("File moved to target folder:"+str(target_path))
        else:
            print("Creating folder")
            logging.info("Creating folder")
            os.mkdir(target_folder)
            shutil.move(source_path, target_path)
            print("Bhavdata file copied from the dowloads folder")
            logging.info("Bhavdata file copied from the dowloads folder")

    def create_one(self, json_record):
        """
        Function to call the API function create to generate a record in the
        SQL table
        Steps:
            1. Create a PoolManager object to manage connections
            2. Create a POST request with the required headers to post the 
                record that is in json_record parameter
            3. If successful, API sends status HTTP status 201
            4. If unsuccessful, API sends HTTP status 503 which means data was
                not loaded into the SQL table
            5. If status is 503, then call store_erroneous_stock_records to 
                store the data in the data folder to be loaded later.
            6. Release the connection

        Parameters
        ----------
        json_record : json 
            This json record is a single record from the dataframe in json
            format

        Returns
        -------
        None.

        """
        http = urllib3.PoolManager()
        try:
            r = http.request('POST', 
                             self.create_one_stock, 
                             headers={'Content-Type':'application/json',
                                      'Accept':'*/*',
                                      'Accept-Encoding':'gzip,deflate,br',
                                      'Connection':'keep-alive',
                                      'User-Agent':'Python-Frontend'},
                             body=json_record)
            print(r.status)
            logging.debug(r.status)
            if str(r.status) == "503":
                logging.info("Capturing the error record")
                self.store_erroneous_stock_records(json_record)
            r.release_conn()
        except urllib3.exceptions.NewConnectionError as e:
            logging.debug("Error creating the connection:"+str(e))
            print(str(e))
    
    def extract_daily_stock_data(self, date=None):
        """
        Extract the daily data from the NSE website and load it into the
        SQL table via the API. The data is loaded one by one into the SQL table
        Steps:
            1. If the date is not provided then call the fn get_date_for_extraction
            2. Generate the filename from the date
            3. Get the data from the NSE website
            4. Move the bhavcopy file into the data folder
            5. Read the csv file into a daaframe
            6. Transform the dataframe into format accepted by the SQL table
            7. Get the count of records to track the progress
            8. Iterate over all the data records
            9. Change each record into a dictionary
            10. Change the record dictionary into json format
            11. Call create_one function to generate a record in the SQL table
            
        Parameters
        ----------
        date : String, optional
            Date is passed to extract the stock data records of a specific day. 
            The default is None.

        Returns
        -------
        None.

        """
        if date == None:
            date = self.get_date_for_extraction()
        file_name = "sec_bhavdata_full_"+date+".csv"
        self.extract_bhavcopy_from_nse(file_name)
        self.get_bhavdata_file(file_name, date)        
        file = os.path.join(self.project_structure["Data"], date, file_name)
        df = pd.read_csv(file).fillna(0)
        df = self.transform_dataframe(df)
        count_of_records = len(df.index) - 1
        error_count = 0
        for index, row in df.iterrows():
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
            
            json_dump = json.dumps(data).encode()
            logging.info("Create record "+str(index)+" :Symbol-"+str(data["symbol"])+", Date-"+str(data["trading_date"])+", Series-"+str(data["series"]))
            print("Progress: "+str(index)+"/"+str(count_of_records)+" completed")
            print("Creating the record for Symbol:"+str(data["symbol"])+", Date:"+str(data["trading_date"])+", Series:"+str(data["series"]))
            self.create_one(json_dump)
        logging.info("Data Extraction completed for "+date) 
    
    def store_erroneous_stock_records(self, error_record):
        """
        Function to store the erroneous records in the file to record 
        and deal with later. This will stop from losing any data and give time
        understand the error
        It will look for a file with name stored in file_name in the data folder,
        erroneous stock subfolder. If not , it will create and then store the
        record in it

        Parameters
        ----------
        error_record : json
            The record that needs to be stored for the analysis in json format.

        Returns
        -------
        None.

        """
        file_name = "error_stock.csv"
        try:
            error_records = pd.read_csv(os.path.join(self.project_structure["Error records"]["Stock"], file_name))
        except Exception as e:
            print(str(e))
            df = pd.DataFrame(list())
            df.to_csv(file_name)
            error_records = pd.read_csv(os.path.join(self.project_structure["Error records"]["Stock"], file_name))
        error_df = pd.read_json(error_record)
        error_records.append(error_df)
        error_records.to_csv(file_name)      
    
    #Function for testing the functions 
    def fn_test(self):
        yesterday = self.get_date_for_extraction()
        print(yesterday)