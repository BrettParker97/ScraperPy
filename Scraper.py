import requests
from bs4 import BeautifulSoup as BS

#input - string
#ouput - float (the number at the begining of the string)
def TakeNumber(string):
    price = ""
    for c in string:
        if c.isnumeric() or c == ".":
            price += c
        else:
            break
    
    #if value cant be a float return -1
    try:
        temp = float(price)
        return temp
    except:
        return (-1)

#input - page information from request()
#ouput - List[0-(n-1)] = steam market urls
#        List[n] = steam game page
def ScrapeUrls(page):
    #find urls other than steampage
    soup = BS(page.content, 'html.parser')
    results = soup.find_all(class_='content-box')
    data = str(results)
    marketUrlData = data.split("https://steamcommunity.com/market/")
    numUrls = (len(marketUrlData) - 2) / 2
    del marketUrlData[0]
    del marketUrlData[0]

    #find steam page url
    urls = []
    for x in range(int(numUrls)):
        temp = marketUrlData[x].split("\"", 1)
        URL = "https://steamcommunity.com/market/" + temp[0]
        urls.append(URL)
    storePage = data.split("https://store.steampowered.com/", 1)
    temp = storePage[1].split("\"")
    storeURL = "https://store.steampowered.com/" + temp[0]
    urls.append(storeURL)
    return urls
    
#input - game exhange page
#output - steamPage url
def ScrapeStoreUrl(page):
    content = str(page.content)
    one = content.split("https://store.steampowered.com/", 1)[1]
    two = content.split("?curator", 1)[0]
    print(two)
    urls = ScrapeUrls(page)
    return urls[len(urls) - 1].split("?curator")

#input - page information from request()
#ouput - price of game (float)
def ScrapeGamePrice(page):
    string = str(page.content)
    temp = string.split("game_purchase_action")
    temp = temp[2].split("discount_final_price")
    temp = temp[len(temp) - 1].split("$", 1)
    temp = temp[1].split("\\")
    y = -1
    for x in temp[0]:
        if x == ".":
            continue
        if x.isnumeric() == False:
            y = x
            break
    if y != -1:
        temp = temp[0].split(y)
    gamePrice = float(temp[0])
    return gamePrice

#input - page information from request()
#ouput - list of strings from page text + filtering
def PrepPageText(page):
    try:
        soup = BS(page.content, 'html.parser')
        results = soup.find_all(class_='content-box')
        
        res = []
        for res2 in results:
            res.append(res2.text)
        del res[0]
        del res[0]
        del res[0]
        return res
    except:
        return -1
    
    

#input - string of text from card page
#output - List if prices
#         False if some check fails
def ScrapeCardPrices(string):
    #checks
    if "Price: NA" in string:
        return False
    elif "Last seen:" in string:
        return False
    
    #find prices
    temp = string.split("$")
    del temp[0]
    priceList = []
    for y in temp:
        price = TakeNumber(y)
        if price == -1:
            continue
        priceList.append(price)
    return priceList

#input - string of text from card page
#output - List[0] = prices[]
#         List[1] = rarities[] 'match with prices index'
#         List[2] = bool (False if some checks failed)
def ScrapeEmoteBG(string):
    #checks
    res3 = True
    if "Price: NA" in string:
        res3 = False
    elif "Last seen:" in string:
        res3 = False
    
    #find prices
    temp = string.split("$")
    del temp[0]
    res1 = []
    for x in temp:
        price = TakeNumber(x)
        if price == -1:
            continue
        res1.append(price)
    
    #count rarites
    res2 = []
    commons = len(string.split("CommonPrice:")) - 1
    uncommons = len(string.split("UncommonPrice:")) - 1
    rares = len(string.split("RarePrice:")) - 1
    for x in range(commons):
        res2.append(0)
    for x in range(uncommons):
        res2.append(1)
    for x in range(rares):
        res2.append(2)
    
    res = [res1, res2, res3]
    return res 

#input - page from request on url
#output - List[0] = normalCards[]
#         List[1] = foilCards[]
#         List[2] = booster price (float)
#         List[3] = emote data [] (refer to ScrapeEmoteBG output)
#         List[4] = background data [] (refer to ScrapeEmoteBG output)
#         List[5] = errors
def ScrapePageData(page):
    prep = PrepPageText(page)
    if prep == -1:
        return [0,0,0,0,0,"prep page failed"]
    normalCards = ScrapeCardPrices(prep[0])
    foilCards = ScrapeCardPrices(prep[1])
    emotes = []
    backgrounds = []
    booster = 0.0
    for x in prep:
        if "EMOTICONS" in x:
            emotes = ScrapeEmoteBG(x)
        if "BACKGROUNDS" in x and "ANIMATED" not in x:
            backgrounds = ScrapeEmoteBG(x)
        if "BOOSTER PACK" in x:
            if "Price: NA" in x or "Last seen" in x:
                booster = False
            else:
                temp = x.split("$")
                booster = TakeNumber(temp[1])
    return [normalCards, foilCards, booster, emotes, backgrounds]
    
def ScrapeAllGameUrls():
    url = "https://www.steamcardexchange.net/index.php?badgeprices"
    
    
