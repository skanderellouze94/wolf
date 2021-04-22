import quandl
import pandas as pd
import pymongo
from pymongo import MongoClient
import investpy

client = MongoClient("mongodb://localhost:27017/")
# database
db = client["investing"]
# collection
company= db["stocks"]

stocks = investpy.get_stocks_list()
#print(stocks)

#f = open("D:\\py app\\traderBot\\demofile2.txt", "a")


for stock in stocks:
    try:
        df = investpy.get_stock_historical_data(stock=stock.upper(), country='united states',from_date='01/01/2019',to_date='04/01/2019')
        #f.write(stock+ ' \n ')
        #print(type(df))
        df.reset_index(inplace=True)
        data_dict = df.to_dict("records")
        company.insert_many({'stock':stock},data_dict)
    except:
        pass
print(len(stocks))
#f.close()
    