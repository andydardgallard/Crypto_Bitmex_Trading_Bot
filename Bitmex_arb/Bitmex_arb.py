from time import sleep
from datetime import datetime
from download_data import download
        
fut = "XBTZ17"
spot = "XBTUSD"
pos = 20000
timeframe = 58  # seconds
filename = "arb_data.txt"
cycle = 1140
k=0

while k < cycle:
    try:        
        download(fut, spot, pos, timeframe, filename)
        
        sleep(timeframe)
        k=k+1
        print datetime.now(), k, "success"
        
    except:
        print k+1, "fail"
        pass