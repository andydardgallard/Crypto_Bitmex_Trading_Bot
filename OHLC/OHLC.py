import requests
import json
from write_csv import write_csv


def data(timeframe):
    tickers=open('C:\\Users\\ADAR\\Documents\\Python Projects\\Crypto_Arb\\OHLC\\OHLC\\Tickers.txt')
    symbol=tickers.read()
    symbol=symbol.split("\n")
    tickers.close()
    
    for i in symbol:
        url="https://www.bitmex.com/api/v1/trade/bucketed?binSize="+str(timeframe)+"m&partial=false&symbol="+i+"&count=1&reverse=true"
        html=requests.get(url).text
        data=json.loads(html)
        
        Timestamp = data[0]['timestamp']        
        Open = data[0]['open']
        High = data[0]['high']
        Low = data[0]['low']
        Close = data[0]['close']
        Volume = data[0]['volume']
        
        new_line = [Timestamp, i, Open, High, Low, Close, Volume]       
        write_csv(i+".txt", new_line)
    return new_line