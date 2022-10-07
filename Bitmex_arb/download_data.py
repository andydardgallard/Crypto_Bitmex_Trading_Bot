import requests
import json
import datetime
from write_csv import write_csv

def download(fut, spot, pos, timeframe, filename):              
    
    fut_url="https://www.bitmex.com/api/v1/orderBook?symbol="+fut+"&depth=25"
    fut_html=requests.get(fut_url).text
    fut_data=json.loads(fut_html)

    spot_url="https://www.bitmex.com/api/v1/orderBook?symbol="+spot+"&depth=25"
    spot_html=requests.get(spot_url).text
    spot_data=json.loads(spot_html)

    fut_setl_url="https://www.bitmex.com/api/v1/instrument?symbol="+fut+"&count=2&reverse=true"
    fut_setl_html=requests.get(fut_setl_url).text
    fut_setl_data=json.loads(fut_setl_html)
    
    YYYY = int(fut_setl_data[0]['settle'][:4])
    MM = int(fut_setl_data[0]['settle'][5:7])
    DD = int(fut_setl_data[0]['settle'][8:10])

    Settle_Date = datetime.date(YYYY,MM,DD)
    Curr_Date = datetime.datetime.utcnow().date()
    Curr_Datetime = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y.%m.%d %H:%M:%S")
    Cur_D = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y.%m.%d")
    Cur_T = datetime.datetime.strftime(datetime.datetime.utcnow(), "%H:%M:%S")
    Days_to_settle = Settle_Date - Curr_Date
    Days_to_settle = int(str(Days_to_settle)[:2])
    Days_for_funding = str(Days_to_settle*3)        
    
    pos_test = pos+pos*0.1
        
    q=0
    w=[]
    e=[]
    for i in fut_data:           
        q=q+i["askSize"]    
        if q>pos_test:
            w.append([i["askSize"], i["askPrice"]])
        if q<pos_test:
            e.append([i["askSize"], i["askPrice"]])      
    r=0
    t=0
    for j in e:
        r=j[0]*j[1]+r
        t=j[0]+t      
    r=w[0][1]*(pos_test-t)+r
    fut_ask=round(r/pos_test)   


    q=0
    w=[]
    e=[]
    for i in fut_data:           
        q=q+i["bidSize"]    
        if q>pos_test:
            w.append([i["bidSize"], i["bidPrice"]])
        if q<pos_test:
            e.append([i["bidSize"], i["bidPrice"]])      
    r=0
    t=0
    for j in e:
        r=j[0]*j[1]+r
        t=j[0]+t      
    r=w[0][1]*(pos_test-t)+r
    fut_bid=round(r/pos_test)
    

    q=0
    w=[]
    e=[]
    for i in spot_data:           
        q=q+i["askSize"]    
        if q>pos_test:
            w.append([i["askSize"], i["askPrice"]])
        if q<pos_test:
            e.append([i["askSize"], i["askPrice"]])      
    r=0
    t=0
    for j in e:
        r=j[0]*j[1]+r
        t=j[0]+t      
    r=w[0][1]*(pos_test-t)+r
    spot_ask=round(r/pos_test)


    q=0
    w=[]
    e=[]
    for i in spot_data:           
        q=q+i["bidSize"]    
        if q>pos_test:
            w.append([i["bidSize"], i["bidPrice"]])
        if q<pos_test:
            e.append([i["bidSize"], i["bidPrice"]])      
    r=0
    t=0
    for j in e:
        r=j[0]*j[1]+r
        t=j[0]+t      
    r=w[0][1]*(pos_test-t)+r
    spot_bid=round(r/pos_test)

    fut_commis = 0.000750
    spot_commis = 0.000750
            
    Spread_Buy = round(fut_ask-spot_bid-(fut_ask*fut_commis)-(spot_bid*spot_commis),2)
    Spread_Sell = round(fut_bid-spot_ask-(fut_bid*fut_commis)-(spot_ask*spot_commis),2)
    
    Spread_Buy_pct = round((((fut_ask-(fut_ask*fut_commis))/(spot_bid+(spot_bid*spot_commis)))
                            **(1/float(Days_to_settle))-1)*36500,4)
    Spread_Sell_pct =round((((fut_bid+(fut_bid*fut_commis))/(spot_ask-(spot_ask*spot_commis)))
                            **(1/float(Days_to_settle))-1)*36500,4)     
            
    new_line=[Cur_D, Cur_T, Days_to_settle, fut_ask, fut_bid, spot_ask, spot_bid, Spread_Buy, Spread_Sell,
              Spread_Buy_pct, Spread_Sell_pct]    
        
    return write_csv(filename, new_line) 