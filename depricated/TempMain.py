import requests
from requests_html import HTMLSession
import time
from Scraper import *
from GraphGrabber import *

#input - manager.dict(), steam game page url
#output - page.content as str
def getPage(return_dict, URL):
    page = requests.get(URL)
    string = str(page.content)
    if "You've made too many requests recently." in string:
        return False
    return return_dict.append(string)

#input - manager.dict(), steam market page url
#output - list [r.content, r.html.text]
def getSCPage(return_dict, URL):
    session = HTMLSession()
    r = session.get(URL)
    r.html.render(sleep = .5)
    if "You've made too many requests recently." in r.html.text:
        print(r.html.text)
        exit()
        return False
    temp = [str(r.content), str(r.html.text)]
    r.close()
    return return_dict.append(temp)

#input - none (main function but im scared to call it main)
#output - list of urls from steamexchange page
def init():
    url = "https://www.steamcardexchange.net/index.php?gamepage-appid-362400"
    page = requests.get(url)
    urls = ScrapeUrls(page)
    return [urls, page]

def getUrlsData(exchangePage, urlPages):
    #steam exchange data
    exchangeData = ScrapePageData(exchangePage)
    
    #steam marketplace data
    for x in range(1, len(urlPages) + 1):
        currentPrices = CurrentPrice(urlPages[x][1])
        graphData = GrabGraph(urlPages[x][0])
    
    #steam game page data
    gamePrice = ScrapeGamePrice(urlPages[len(urlPages) + 1])
    
    #push to stats or save data?

if __name__ == "__main__":
    data = init()
    urls = data[0]
    page = data[1]
    res = []
    
    start = time.time()
    
    waitTimerList = []
    for x in range(len(urls)):
        print("Doing proc #" + str(x))
        waitTimer = 0
        while True:
            print("current waitTimer " + str(waitTimer))
            res2 = 0
            if "steamcommunity" in urls[x]:
                res2 = getSCPage(res, urls[x])
            else:
                res2 = getPage(res, urls[x])
            
            if res2 is False:
                waitTimer += 1
                time.sleep(waitTimer)
            else:
                waitTimerList.append(waitTimer)
                res.append(res2)
                break
    print("average wait time " + str(mean(waitTimerList)))
    print("len of res " + str(len(res)))
    
    exit()
    
    pages = []
    for x in return_dict.values():
        pages.append(x)
    
    y = 0
    for x in range(1,len(pages) + 1):
        if type(pages[x]) is list:
            
            if "Please wait and try your request again" in pages[x][0]:
                print("fuck " + str(y))
                y+=1
    exit()
    
    getUrlsData(page, pages)
    
    end = time.time()
    print("elapsed time = " + str(end - start))