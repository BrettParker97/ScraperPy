#VM - Desktop\Coding\ScraperPy\env\Scripts\activate.bat
#DIC - cd Desktop\Coding\ScraperPy

import requests
import time
import sys
import math
from Scraper import *
from Statistics import *

import multiprocessing as mp

sys.path.append(".")
from DataClass import DataClass
from DB import Database

def getUrlData(url):
    #steam exchange data
    page = requests.get(url)
    pageData = ScrapePageData(page)
    page.close()
    return pageData

def main(url, dataB, que):
    gemPrice = .42
    
    #create data class to store information in
    dataToStore = DataClass()
    exchangeUrl = "https://www.steamcardexchange.net/" + url
    dataToStore.cardExchange = exchangeUrl
    
    #scrape data off exchange page
    pageData = getUrlData(exchangeUrl)
    if len(pageData) == 6:
        print("load pageFailed")
        dataToStore.badData = True
        dataToStore.reason = pageData[5]
        dataToStore.queryPrep()
        que.put(dataToStore)
        exit()
    
    #steam url 
    gameID = url.split("-appid-", 1)[1]
    dataToStore.gameID = gameID
    dataToStore.steamUrl = "https://store.steampowered.com/app/" + str(gameID)
    
    #get normal and foil card information
    if pageData[0] == False or pageData[1] == False:
        #we failed a card check refer to scraper doc
        errorVal = None
        if pageData[0] == False:
            errorVal = 0
        else:
            errorVal = 1
        dataToStore.badData = True
        dataToStore.reason = "Card check failed - data either had NA or Last seen variable. pageData[" + str(errorVal)+ "] was the source"
        
        #store the failure data
        dataToStore.queryPrep()
        que.put(dataToStore)
        exit()
        
    #outliers and avgPrice data
    dataToStore.cardOutliers = outlierCheck(pageData[0])
    dataToStore.foilOutliers = outlierCheck(pageData[1])
    avgCP = avgCardPrice(pageData[0])
    dataToStore.avgPriceCard = round(avgCP, 2)
    avgFoilPrice = avgCardPrice(pageData[1])
    avgCardPriceF = avgCP + ((1/100) * avgFoilPrice)
    dataToStore.avgPriceCardF = round(avgCardPriceF, 2)
    
    #start card data
    numCardsInBadge = len(pageData[0])
    boosterBuyPrice = None
    if pageData[2] != False:
        boosterBuyPrice = pageData[2]
    
    #pack buy price/profit
    expectedReturn = avgCardPriceF * 3
    if boosterBuyPrice == None:
        dataToStore.packBuyPrice = 0
        dataToStore.packBuyProfit = 0
    else:
        dataToStore.packBuyPrice = boosterBuyPrice
        dataToStore.packBuyProfit = round(expectedReturn - boosterBuyPrice, 2)
    
    #pack make price/profit
    gemReq = math.ceil(6000 / numCardsInBadge)
    gemReq = gemReq / 1000
    gemTotalPrice = gemPrice * gemReq
    packsToMake = math.ceil(numCardsInBadge / 3)
    dataToStore.packMakePrice = round(gemTotalPrice, 2)
    extraCards = numCardsInBadge - (packsToMake * 3)
    finalMakePrice = (gemTotalPrice * packsToMake) - (extraCards * avgCardPriceF)
    dataToStore.packMakeProfit = round(expectedReturn - gemTotalPrice, 2)
    
    #badge buy/make price
    dataToStore.badgeBuyPrice = round(sum(pageData[0]), 2)
    dataToStore.badgeMakePrice = round(finalMakePrice, 2)
    
    #check emotes and backgrounds
    if pageData[3][2] == False or pageData[4][2] == False:
        #we failed a card check refer to scraper doc
        errorVal = None
        if pageData[3][2] == False:
            errorVal = 3
        else:
            errorVal = 4
        dataToStore.badData = True
        dataToStore.reason = "Emote/BG check failed - data either had NA or Last seen variable. pageData[" + str(errorVal)+ "] was the source"
        
        #store the failure data
        dataToStore.queryPrep()
        que.put(dataToStore)
        exit()
    
    #emote price
    emotePrices = pageData[3][0]
    emoteRarity = pageData[3][1]
    expectedEmote = expectedPriceEmoteBG(emotePrices, emoteRarity)
    dataToStore.expectEmote = round(expectedEmote, 2)

    #background price
    bgPrices = pageData[4][0]
    bgRarity = pageData[4][1]
    expectedBG = expectedPriceEmoteBG(bgPrices, bgRarity)
    dataToStore.expectBG = round(expectedBG, 2)
    
    #badge creation expected profit
    priceOfBuyCards = sum(pageData[0])
        
    dataToStore.expectBuyBadgeProfit = round(expectedEmote + expectedBG - priceOfBuyCards, 2)
    priceOfMakeCards = dataToStore.badgeMakePrice
    dataToStore.expectMakeBadgeProfit = round(expectedEmote + expectedBG - priceOfMakeCards, 2)
    
    #add to dataB
    dataToStore.queryPrep()
    que.put(dataToStore)
    exit()
   
#input - mp.que, dataBase
#output - None
#used to try and limit connections to database
def sendToDB(que, dataB):
    while que.qsize() > 0:
        query = que.get()
        dataB.addToDB(query)
    exit()
        
if __name__ == "__main__":
    #create database access class
    dataB = Database()
    
    #open datafile and read all urls into a list
    dataFile = open("data4.txt", "r")
    data = dataFile.read()
    urls = data.splitlines()
    
    #set up multiproccessing 
    mp.set_start_method('spawn')
    que = mp.Queue()
    queReader = mp.Process(target = sendToDB, args=(que, dataB, ))
    queReader.start()
    
    counter = 0
    s = time.time()
    #for each url, start a proccess to scrape and collect
    #the data from the url
    #program limited to 3 requests a second
    for x in urls:
        temp = x.split("appid-", 1)[1]
        print((f"working on #{counter},"
               f"elapsed time = {math.ceil(time.time()-s)},"
               f"gameID = {temp}"))
        
        #check if the game is already in the database
        #move on if it is
        #temp is init above the print so i can display it
        if dataB.checkExists(temp) == True:
            print("In DB - Skipped")
            continue
        
        #increase counter after we check if data is
        #already in db, just to keep time more
        #accurate
        counter += 1
       
        #start the proccess
        proc = mp.Process(target = main, args=(x, dataB, que, ))
        proc.start()
        
        #start up the reader if we need to
        queReader.join()
        if queReader.is_alive() != True and que.qsize() > 0:
            queReader = mp.Process(target = sendToDB, args=(que, dataB, ))
            queReader.start()
        
        #wait .333 ms aka 3 reqs / sec
        time.sleep(.333)
    e = time.time()
    
    #give any not finished procs 2 seconds to finish up
    time.sleep(2)
    
    #run que reader until que is empty
    while que.qsize() > 0 or queReader.is_alive() == True:
        queReader.join()
        if queReader.is_alive() != True and que.qsize() > 0:
                queReader = mp.Process(target = sendToDB, args=(que, dataB, ))
                queReader.start()
        time.sleep(1)
        
    print(f"{(e-s) / 100} was average run time (including dups)")
    print ("--end of program--")
    exit()

