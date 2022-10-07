import requests
import json
from write_csv import write_csv


def data(timeframe):
    tickers=open('C:\\Users\\ADAR\\Documents\\Python Projects\\Crypto_Arb\\OHLC\\OHLC\\Tickers.txt')
    symbol=tickers.read()
    symbol=symbol.split("\n")
    tickers.close()
    
    for i in symbol:
        url="https://www.bitmex.com/api/v1/trade/bucketed?binSize="+str(timeframe)+"h&partial=false&symbol="+i+"&count=1&reverse=true"
        html=requests.get(url).text
        data=json.loads(html)
        
        YYYY = data[0]['timestamp'][:4]
        MM = data[0]['timestamp'][5:7]
        DD = data[0]['timestamp'][8:10]        
        Date = YYYY+MM+DD
        
        HH = data[0]['timestamp'][11:13]
        Min = data[0]['timestamp'][14:16]
        Time = HH+Min
        
        Open = data[0]['open']
        High = data[0]['high']
        Low = data[0]['low']
        Close = data[0]['close']
        Volume = data[0]['volume']
        
        new_line = [Date, Time, i, Open, High, Low, Close, Volume]       
        write_csv(i+".txt", new_line)
    return new_line