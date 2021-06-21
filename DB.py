import mysql.connector
from mysql.connector import errorcode
from DataClass import DataClass

class Database:
    def __init__(self):
        self.cnx = None
        self.cursor = None
        try:
          self.cnx = mysql.connector.connect(user='root',
                                        database='scraperpy')
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        else:
            self.cnx = None
            print("connection worked")
    
    def closeDB(self):
        self.cursor.close()
        self.cnx.close()
    
    def addToDB(self, dataToStore):
        self.cnx = mysql.connector.connect(user='root', database='scraperpy')
        self.cursor = self.cnx.cursor()
        add_employee = ("INSERT INTO data "
               f"(gameID, steamUrl,"
               f" cardExchange, cardOutliers,"
               f" foilOutliers, badData,"
               f" reason, avgPriceCard,"
               f" avgPriceCardF, packBuyPrice,"
               f" packBuyProfit, packMakePrice,"
               f" packMakeProfit, badgeBuyPrice,"
               f" badgeMakePrice, expectEmote,"
               f" expectBG, expectBuyBadgeProfit,"
               f" expectMakeBadgeProfit)"
               "VALUES"
               f"({dataToStore.gameID}, \"{dataToStore.steamUrl}\","
               f" \"{dataToStore.cardExchange}\", {dataToStore.cardOutliers},"
               f" {dataToStore.foilOutliers}, {dataToStore.badData},"
               f" \"{dataToStore.reason}\", {dataToStore.avgPriceCard},"
               f" {dataToStore.avgPriceCardF}, {dataToStore.packBuyPrice},"
               f" {dataToStore.packBuyProfit}, {dataToStore.packMakePrice},"
               f" {dataToStore.packMakeProfit}, {dataToStore.badgeBuyPrice},"
               f" {dataToStore.badgeMakePrice}, {dataToStore.expectEmote},"
               f" {dataToStore.expectBG}, {dataToStore.expectBuyBadgeProfit},"
               f" {dataToStore.expectMakeBadgeProfit})")
        
        res = True
        try:
            self.cursor.execute(add_employee)
        except mysql.connector.Error as err:
            print(err)
            if "Duplicate entry" in str(err):
                res = self.updateToDB(dataToStore)
        if res == True:
            self.cnx.commit()
            self.closeDB()
            return
        else:
            self.closeDB()
            return

    def updateToDB(self, dataToStore):
            add_employee = ("UPDATE data "
                   "SET"
                   f" steamUrl = \"{dataToStore.steamUrl}\","
                   f" cardExchange = \"{dataToStore.cardExchange}\", cardOutliers = {dataToStore.cardOutliers},"
                   f" foilOutliers = {dataToStore.foilOutliers}, badData = {dataToStore.badData},"
                   f" reason = \"{dataToStore.reason}\", avgPriceCard = {dataToStore.avgPriceCard},"
                   f" avgPriceCardF = {dataToStore.avgPriceCardF}, packBuyPrice = {dataToStore.packBuyPrice},"
                   f" packBuyProfit = {dataToStore.packBuyProfit}, packMakePrice = {dataToStore.packMakePrice},"
                   f" packMakeProfit = {dataToStore.packMakeProfit}, badgeBuyPrice = {dataToStore.badgeBuyPrice},"
                   f" badgeMakePrice = {dataToStore.badgeMakePrice}, expectEmote = {dataToStore.expectEmote},"
                   f" expectBG = {dataToStore.expectBG}, expectBuyBadgeProfit = {dataToStore.expectBuyBadgeProfit},"
                   f" expectMakeBadgeProfit = {dataToStore.expectMakeBadgeProfit}"
                   " WHERE "
                   f"gameID = {dataToStore.gameID}")
            try:
                self.cursor.execute(add_employee)
            except mysql.connector.Error as err:
                print(err)
                return False
            return True
    
    def checkExists(self, gameID):
        self.cnx = mysql.connector.connect(user='root', database='scraperpy')
        self.cursor = self.cnx.cursor()
    
        query = (f"SELECT * FROM `data` WHERE gameID = {gameID}")
    
        res = True
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)
            if "Duplicate entry" in str(err):
                res = self.updateToDB(dataToStore)
        
        res = self.cursor.fetchone()
        if res != None:
            return True
        else:
            return False
        
    
    
    
    
    
    
    
    
    
        

