from scipy import stats
import math

#input - list of prices
#output - number of outliers in input
def outlierCheck(prices):
    a = stats.zscore(prices)
    counter = 0
    for x in a:
        #generally 3 SDs is considered outlierCheck
        if x > 3 or x < -3:
            counter += 1
    return counter

#input - list of prices
#output - average price in list (after excluding tax)
def avgCardPrice(prices):
    temp = []
    for x in range(len(prices)):
        if (.13 * prices[x]) > .025:
            temp.append(round(prices[x] - (.13 * prices[x]), 2))
        else:
            temp.append(round(prices[x] - .02, 2))
    summ = sum(temp)
    return round(summ / len(temp), 2)

#input - list of prices, list of corrisponding rarity
#output - expected return value per badge
def expectedPriceEmoteBG(prices, rarity):
    emotePrices = prices
    emoteRarity = rarity
    emoteCom = []
    emoteUn = []
    emoteR = []
    for x in range(len(emotePrices)):
        rarity = emoteRarity[x]
        if rarity == 0:
            emoteCom.append(emotePrices[x])
        elif rarity == 1:
            emoteUn.append(emotePrices[x])
        else:
            emoteR.append(emotePrices[x])
    expectedEmote = (sum(emoteCom) / len(emoteCom)) * .69
    expectedEmote += (sum(emoteUn) / len(emoteUn)) * .19
    expectedEmote += (sum(emoteR) / len(emoteR)) * .12
    
    if (.13 * expectedEmote) > .025:
        return round(prices[x] - (.13 * expectedEmote), 2)
    else:
        return round(prices[x] - .02, 2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
