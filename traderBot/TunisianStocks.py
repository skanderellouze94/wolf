import pandas as pd
import pymongo
from pymongo import MongoClient
import investpy
import matplotlib.pyplot as plt
import time
from datetime import datetime

x=500
client = MongoClient("mongodb://localhost:27017/")
# database
db = client["investingInTunisia"]
# collection
company= db["stocks"]

stocks = investpy.get_stocks_list( country='tunisia')
def getStocks():
    for stock in stocks:
        try:
            df = investpy.get_stock_historical_data(stock=stock.upper(), country='tunisia',from_date='15/01/2021',to_date='16/01/2021')
            df.reset_index(inplace=True)
            df.append({'stock':stock},ignore_index=True)
            data_dict = df.to_dict("records")
            today = datetime.now()
            data_dict[0]['Date']=today.strftime("%Y-%m-%d %H:%M:%S")
            print(stock)
            company.insert_one({"index":stock,"data":data_dict})
        except:
            pass


def getStocksInRealTime():
    for stock in stocks:
        try:
            df = investpy.get_stock_historical_data(stock=stock.upper(), country='tunisia',from_date='15/01/2021',to_date='16/01/2021')
            df.reset_index(inplace=True)
            df.append({'stock':stock},ignore_index=True)
            data_dict = df.to_dict("records")
            print(stock)
            filtre = {"index":stock}
            today = datetime.now()
            data_dict[0]['Date']=today.strftime("%Y-%m-%d %H:%M:%S")
            company.update_one(filtre,{"$push": {"data":data_dict[0]}})
        except:
            pass

def getStockOf(stock):
    try:
        df = investpy.get_stock_historical_data(stock=stock.upper(), country='tunisia',from_date='28/12/2019',to_date='29/12/2020')
        df.reset_index(inplace=True)
        df.append({'stock':stock},ignore_index=True)
        data_dict = df.to_dict("records")
        print(stock)
        company.insert_one({"index":stock,"data":data_dict})
    except:
        pass        

def showDataFrame():
    for stock in stocks:
        data_from_db = company.find_one({"index":stock})
        df = pd.DataFrame(data_from_db["data"])
        df.set_index("Date",inplace=True)
        print(df)

def showStockDataFrame(stock):
    data_from_db = company.find_one({"index":stock})
    print(data_from_db)
    df = pd.DataFrame(data_from_db["data"])
    print(df)
    df.set_index("Date",inplace=True)
    df['SMA(3)']=df.Close.rolling(3).mean()
    df['SMA(6)']=df.Close.rolling(6).mean()
    count=[]
    for i in range(len(df)):
        try:
            count.append(((df.Close[i]-df.Close[i+1])*100)/df.Close[i+1])
        except:
            pass
    count.append(0)
    df['%Count']=count
    
    plt.figure(figsize=(12.5,4.5))
    plt.plot(df['Close'],label='close',color='black')
    #plt.plot(df['%Count'],label='Count')
    plt.plot(df['SMA(3)'],label='SMA3')
    plt.plot(df['SMA(6)'],label='SMA6')
    plt.title(stock)
    plt.xlabel("01/01/2015 - 01/01/2020")
    plt.ylabel("close and open price TND")
    plt.legend(loc='upper left')
    plt.show() 
  


def deleteCollections():
    for stock in stocks:
        company= db[stock]
        company.drop()
        print(stock+' deleted')

def getCountries():
    print(investpy.get_stock_countries())

#getCountries()
showStockDataFrame('BIAT')
#getStockOf('AB')
#getStocks()
#while True:
#    getStocksInRealTime()
#    time.sleep(3)