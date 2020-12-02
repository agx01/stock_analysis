
# -*- coding: utf-8 -*-

import json
import os
import pandas as pd

#Setting up the project structure
data_dict = {}
data_dict["Project Structure"] = {}
data_dict["Project Structure"]["Error records"] ={}
data_dict["Links"] = {}
data_dict["Links"]["stocks"] = {}
data_dict["Links"]["indices"] = {}
config_filename = "config.json"

#root folder path
root = "C:\\"+os.path.join("Users", "Arijit Ganguly", "Documents", "PythonProjects", "stock_analysis")

#Data path
data_dict["Project Structure"]["Data"] = os.path.join(root, "data")

#Historic Stocks Data path
data_dict["Project Structure"]["Historic stocks"] = os.path.join(root, "data", "historic_data", "stocks")

#Logs path
data_dict["Project Structure"]["Logs"] = os.path.join(root, "data", "logs")

#Error records stock
data_dict["Project Structure"]["Error records"]["Stock"] = os.path.join(root, "data", "erroneous_stock")

#Error records indices
data_dict["Project Structure"]["Error records"]["Indices"] = os.path.join(root, "data", "erroneous_index")

#Executables path
data_dict["Project Structure"]["Executables"] = os.path.join(root, "bin")

#Application path
data_dict["Project Structure"]["Application"] = os.path.join(root, "stock_analysis")

#Test code path
data_dict["Project Structure"]["Test"] = os.path.join(root, "test")

#NSE download path
data_dict["Project Structure"]["Download"] = "C:\\"+os.path.join("Users","Arijit Ganguly","Downloads")

#Chrome driver path
data_dict["Project Structure"]["Chrome driver"] = "C:\\"+os.path.join("Work","chromedriver_win32", "chromedriver")

#NSE archive web link
data_dict["Links"]["Base nse url"] = "https://archives.nseindia.com/products/content/"

#NSE index archive weblink
data_dict["Links"]["Base index url"] = "https://archives.nseindia.com/content/indices/"

#API stocks link
data_dict["Links"]["stocks"]["base"] = "http://www.arijitganguly.com/api/stock/"

#API indices link
data_dict["Links"]["indices"]["base"] = "http://www.arijitganguly.com/api/indices/"

#API function links
data_dict["Links"]["stocks"]["Read"] = "http://www.arijitganguly.com/api/stock/read.php"
data_dict["Links"]["stocks"]["Create"] = "http://www.arijitganguly.com/api/stock/create.php"
data_dict["Links"]["stocks"]["Search by Symbol"] = "http://www.arijitganguly.com/api/stock/search_by_symbol.php?symbol="
data_dict["Links"]["stocks"]["Unique Stocks"] = "http://www.arijitganguly.com/api/stock/get_unique_stocks.php"
data_dict["Links"]["indices"]["Create"] = "http://www.arijitganguly.com/api/indices/create.php"

#Check if the config file exists
if not os.path.isfile(os.path.join(data_dict["Project Structure"]["Application"], config_filename)):
    # if not, create the config file
    with open(os.path.join(data_dict["Project Structure"]["Application"], config_filename), "w") as outfile:
        json.dump(data_dict, outfile)
    print("Config file created")
else:
    #if yes, then no action required and inform file exists
    print("Config file already exists")
