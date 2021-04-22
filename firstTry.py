import investpy
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time

plt.style.use('fivethirtyeight')

df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2015',
                                        to_date='01/01/2020')
                                      
AAPL=df
plt.figure(figsize=(12.5,4.5))
plt.plot(AAPL['Close'],label='AAPL')
plt.title('Apple close price')
plt.xlabel("01/01/2015 - 01/01/2020")
plt.ylabel("close price $")
plt.legend(loc='upper left')
plt.show()

#stocks = investpy.get_stocks_list()
#print(stocks)
