#VM - Desktop\Coding\ScraperPy\env\Scripts\activate.bat
#DIC - cd Desktop\Coding\ScraperPy

import requests
import time
import sys
import math
from Scraper import *
from Statistics import *

sys.path.append(".")
from DataClass import DataClass
from DB import Database

def getUrlData(url):
    #steam exchange data
    page = requests.get(url)
    pageData = ScrapePageData(page)
    page.close()
    
    return pageData

def main():
    dataB = Database()
    
    dataFile = open("data5.txt", "r")
    data = dataFile.read()
    urls = data.splitlines()
    
    #print("Enter current 'sack o' gems' price as: .XX")
    #gemPrice = input()
    #gemPrice = float(gemPrice)
    gemPrice = .42

    times = []
    for x in range(len(urls)):
        print(f"Working {x}")
        #start timer to make sure I dont spam
        start = time.time()
        
        #create data class to store information in
        dataToStore = DataClass()
        exchangeUrl = "https://www.steamcardexchange.net/" + urls[x]
        dataToStore.cardExchange = exchangeUrl
        
        #scrape data off exchange page
        pageData = getUrlData(exchangeUrl)
        
        #steam url 
        gameID = urls[x].split("-appid-", 1)[1]
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
            dataB.addToDB(dataToStore)
            
            #end timer
            end = time.time()
            times.append(end - start)
            continue
            
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
            dataB.addToDB(dataToStore)
            
            #end timer
            end = time.time()
            times.append(end - start)
            continue
        
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
        dataB.addToDB(dataToStore)
        
        #end timer
        end = time.time()
        times.append(end - start)
        
        #limit our program to 3 reqs a second which is .2s per req
        if end - start < .20:
            print("Going to fast, sleeping for a time")
            time.sleep(.2 - (end - start))
   
    print("average run time was: ", str((sum(times) / len(times))), " seconds")
    dataB.closeDB()
    
    
if __name__ == "__main__":
    main()
    print ("--end of program--")
    exit()



