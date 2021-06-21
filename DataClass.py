class DataClass:
    def __init__(self):
        self.gameID = None
        self.steamUrl = None
        self.cardExchange = None
        
        self.cardOutliers = None
        self.foilOutliers = None
        
        #if data didnt pass a check durring collection
        #list flag badData and put the check in the reason
        self.badData = None
        self.reason = None
        
        self.avgPriceCard = None
        self.avgPriceCardF = None
        
        self.packBuyPrice = None
        self.packBuyProfit = None
        self.packMakePrice = None
        self.packMakeProfit = None
        
        self.badgeBuyPrice = None
        self.badgeMakePrice = None
        
        self.expectEmote = None
        self.expectBG = None
        self.expectBuyBadgeProfit = None
        self.expectMakeBadgeProfit = None
        
    def __repr__(self):
        res = ("DataClass(steamUrl=" + str(self.steamUrl) + ", cardExchange="
        + str(self.cardExchange) + ", foilOutliers="+ str(self.foilOutliers) + ", cardOutliers="
        + str(self.cardOutliers) + ", badData="+ str(self.badData) + ", reason="
        + str(self.reason) + ", avgPriceCard="+ str(self.avgPriceCard) + ", avgPriceCardF="
        + str(self.avgPriceCardF) + ", packBuyPrice="+ str(self.packBuyPrice) + ", packBuyProfit="
        + str(self.packBuyProfit) + ", packMakePrice="+ str(self.packMakePrice) + ", packMakeProfit="
        + str(self.packMakeProfit) + ", badgeBuyPrice="+ str(self.badgeBuyPrice) + ", badgeMakePrice="
        + str(self.badgeMakePrice) + ", expectEmote="+ str(self.expectEmote) + ", expectBG="
        + str(self.expectBG) + ", expectBuyBadgeProfit="+ str(self.expectBuyBadgeProfit) + ", expectMakeBadgeProfit="
        + str(self.expectMakeBadgeProfit))
        return res
        
    #changes all None values to "NULL" for mySQL query
    def queryPrep(self):
        if self.gameID == None:
            self.gameID = "NULL"
        if self.steamUrl == None:
            self.steamUrl = "NULL"
        if self.cardExchange == None:
            self.cardExchange = "NULL"
        if self.cardOutliers == None:
            self.cardOutliers = "NULL"
        if self.foilOutliers == None:
            self.foilOutliers = "NULL"
        if self.badData == None:
            self.badData = "NULL"
        if self.reason == None:
            self.reason = "NULL"
        if self.avgPriceCard == None:
            self.avgPriceCard = "NULL"
        if self.avgPriceCardF == None:
            self.avgPriceCardF = "NULL"
        if self.packBuyPrice == None:
            self.packBuyPrice = "NULL"
        if self.packBuyProfit == None:
            self.packBuyProfit = "NULL"
        if self.packMakePrice == None:
            self.packMakePrice = "NULL"
        if self.packMakeProfit == None:
            self.packMakeProfit = "NULL"
        if self.badgeBuyPrice == None:
            self.badgeBuyPrice = "NULL"
        if self.badgeMakePrice == None:
            self.badgeMakePrice = "NULL"
        if self.expectEmote == None:
            self.expectEmote = "NULL"
        if self.expectBG == None:
            self.expectBG = "NULL"
        if self.expectBuyBadgeProfit == None:
            self.expectBuyBadgeProfit = "NULL"
        if self.expectMakeBadgeProfit == None:
            self.expectMakeBadgeProfit = "NULL"