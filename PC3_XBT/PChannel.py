import talib
import numpy as np
from Param import param
from write_csv import write_csv

def PChannel():

    ohlc=open('C:\\Users\\ADAR\\Documents\\Python Projects\\Crypto_Arb\\OHLC_60\\OHLC_60\\'+param()["symbol"]+'.txt')
    data=ohlc.read().splitlines()  
    ohlc.close()

    DATA = []
    for i in data:
        DATA.append(i.split(","))
    #    print i.split(",")

    high = []
    for i in zip(*DATA)[4]:
        high.append(i)
    #    print high
    high = [float(x) for x in high]
    high_SMA = talib.SMA(np.array(high), param()["AverPricePeriod"]*param()["Timeframe"])
    pcUP = talib.MAX(high_SMA, param()["PChannel"]*param()["Timeframe"])
    

    low = []
    for i in zip(*DATA)[5]:
        low.append(i)
    #    print low
    low = [float(x) for x in low]
    low_SMA = talib.SMA(np.array(low), param()["AverPricePeriod"]*param()["Timeframe"])
    pcDOWN = talib.MIN(low_SMA, param()["PChannel"]*param()["Timeframe"])
    
    close = float(zip(*DATA)[6][-1])

    signal = 0
    
    if close > pcUP[-2:-1]: signal = "buy"
    if close < pcDOWN[-2:-1]: signal = "sell"
    
    #for i in range(len(np.array(high))):
    write_csv("1.csv", [signal, close, pcUP[-2:-1], pcDOWN[-2:-1]])
    
    
    return 
