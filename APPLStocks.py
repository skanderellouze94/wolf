import pandas as pd
import pymongo
from pymongo import MongoClient
import investpy
import matplotlib.pyplot as plt
import time
from datetime import datetime
from matplotlib.animation import FuncAnimation
from shapely.geometry import LineString
import numpy as np

i=1
x=500
client = MongoClient("mongodb://localhost:27017/")
# database
db = client["investing"]
# collection
company= db["stocks"]
test=True
def getOneStocks():
    try:
        df = investpy.get_stock_historical_data(stock="AAPL", country='United States',from_date='15/01/2021',to_date='16/01/2021')
        df.reset_index(inplace=True)
        df.append({'stock':"AAPL"},ignore_index=True)
        data_dict = df.to_dict("records")
        print(data_dict[0]['Date'])
        today = datetime.now()
        data_dict[0]['Date']=today.strftime("%Y-%m-%d %H:%M:%S")
        print(data_dict[0]['Date'])
        
        company.insert_one({"index":"AAPL","data":data_dict})

    except:
        pass


def getStocks():
    try:
        df = investpy.get_stock_historical_data(stock="AAPL", country='United States',from_date='15/01/2021',to_date='16/01/2021')
        df.reset_index(inplace=True)
        df.append({'stock':"AAPL"},ignore_index=True)
        data_dict = df.to_dict("records")
        print(data_dict)
        print('AAPL')
        filtre = {"index":"AAPL"}
        today = datetime.now()
        data_dict[0]['Date']=today.strftime("%Y-%m-%d %H:%M:%S")
        company.update_one(filtre,{"$push": {"data":data_dict[0]}})
        
    except:
        pass

 

def showStockDataFrame(stock):
    data_from_db = company.find_one({"index":stock})
    df = pd.DataFrame(data_from_db["data"])
    df.set_index("Date",inplace=True)
    df['SMA(2)']=df.Close.rolling(2).mean()
    df['SMA(5)']=df.Close.rolling(5).mean()
    
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
    plt.plot(df['SMA(2)'],label='SMA3')
    plt.plot(df['SMA(5)'],label='SMA6')
    plt.title(stock)
    plt.xlabel("01/01/2015 - 01/01/2020")
    plt.ylabel("close and open price TND")
    plt.legend(loc='upper left')

    plt.show() 



showStockDataFrame('AAPL')
#getOneStocks()
#while True:
#    getStocks()
#    time.sleep(3)
