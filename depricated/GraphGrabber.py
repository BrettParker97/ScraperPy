import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS

#input - r.content str from community market url
#output - dict where <date> -> <tuple(tuple(price,amount))>
def GrabGraph(string):
    t = string.split("market_commodity_forsale_table")
    t = t[1].split("market_commodity_orders_block")
    print(len(t))
    print(t[0])
    
    data = string.split("line1=[[")
    data = data[1].split("]]")
    data = data[0].split(" 2021", 1)
    data = data[1].split("],[", 1)
    data = data[1].split("\"],[\"")
    del data[0]
    # <date> -> <tuple(tuple(price,amount))>
    byDateDict = {}
    SortData(byDateDict, data)
    return byDateDict
    
def SortData(byDateDict, data):
    for x in data:
        temp = x.split(" 2021")
        date = temp[0]
        rightSide = temp[1]
        temp = rightSide.split(",", 2)
        price = float(temp[1])
        amount = int(temp[2].split("\"")[1])
        value = byDateDict.get(date)
        if value != None:
            value = list(value)
            value.append(tuple([price,amount]))
            byDateDict[date] = tuple(value)
        else:
            byDateDict[date] = tuple([tuple([price,amount])])

#input - string of data from CurrentPrice()
#output - List [CurrentPrice, CurrentAmount] 
def CurrentPriceSupportFun(string):
    buyPrice = []
    buyAmount = []
    for x in string:
        temp = x.split("\n")
        for y in temp:
            if "." in y:
                if "or more" in y:
                    break
                if "or lower" in y:
                    break
                buyPrice.append(float(y))
            elif y.isnumeric():
                buyAmount.append(int(y))
    return [buyPrice, buyAmount]

#input - r.html.text string of steam marketplace
#ouput - List [Buy[price, amount], Sell[price, amount]]
def CurrentPrice(string):
    print("22222222")
    print(string)
    data = string.split("Quantity")
    temp = data[1].split("$")
    buy = CurrentPriceSupportFun(temp)
    temp = data[2].split("Recent activity")
    temp = temp[0].split("$")
    sell = CurrentPriceSupportFun(temp)

