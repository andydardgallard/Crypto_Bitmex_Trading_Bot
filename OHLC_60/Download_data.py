from time import sleep
from datetime import datetime
from OHLC_60 import data
        

timeframe = 1  # houres

cycle = 1140
k=0

while k < cycle:
    try:        
        data(timeframe) 
                
        k=k+1
        print datetime.now(), k, "success"
        sleep(timeframe*3600)
        
    except:
        print k+1, "fail"
        pass