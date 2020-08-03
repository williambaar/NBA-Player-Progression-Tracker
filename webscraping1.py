# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 00:26:54 2020

@author: William Baar

This program will:
    1. Utilize the BeautifulSoup and Requests packages to web scrape NBA player 
       statistics from BasketballReference.com.
    2. Store the data into two lists of tuples for easier entry into a MySQL database.
    3. Connect to the MySQL Database server and insert the data into two tables:
       Player and BeforeQ.
"""

#Packages for webscraping
from bs4 import BeautifulSoup
import requests

#Package for connecting to MySQL database
import mysql.connector



#Request URL
source = requests.get("https://www.basketball-reference.com/leagues/NBA_2020_per_game.html").text

#Grab website HTML
soup = BeautifulSoup(source, "lxml")

#Parse the table of statistics
playerStats = soup.find("tbody")
#print(playerStats.prettify())

#list_container will be a list of lists containing all player statistics
list_container = list()

#Each row contains a player, his rank (ID), and statistics like PPG, APG, RPG, etc.
#Parse all this information and store it in a list
for player in playerStats.find_all("tr", class_="full_table"): #Each row
    
    each = list()
    
    for stats in player.find_all("td"): #Each player's statistics (PPG, APG, RPG, etc.)    
    
        #Check if the player statistic is stored as the empty string      
        if(len(stats.text)==0):        
        
            #Convert empty string to a Null (None) value and append
            each.append(None)        
        
        else:        
        
            each.append(stats.text)        
    
    list_container.append(each)

#Create a new list_container that holds all Player table information
player_table = list()
for column in list_container:
    each = list()
    each.append(column[0])
    each.append(column[1])
    each.append(column[2])
    each.append(column[3])
    player_table.append(each)

#Convert list of lists to list of tuples for easier entry into MySQL database
player_tuple = [tuple(l) for l in player_table]

#print(player_tuple)

#Create a new tuple_container that holds all BeforeQ table information
beforeq_table = list()
for column in list_container:
    each = list()
    each.append(column[0])
    each.append(column[28])
    each.append(column[7])
    each.append(column[8])
    each.append(column[9]) 
    each.append(column[10])
    each.append(column[11])
    each.append(column[12]) 
    each.append(column[17])
    each.append(column[18])
    each.append(column[19]) 
    each.append(column[20])
    each.append(column[21])
    each.append(column[22])
    each.append(column[23])
    each.append(column[26])
    each.append(column[24])
    each.append(column[25])
    each.append(column[27])
    beforeq_table.append(each)
    
#Convert list of lists to list of tuples for easier entry into MySQL database
beforeq_tuple = [tuple(l) for l in beforeq_table]

#print(beforeq_tuple)


 #---------------------------------------------------------------------------------------
 
#Connect to MySQL connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="####", database="NBA_Player_Stats")

mycursor = mydb.cursor()

sqlform1 = (
           "INSERT INTO Player(Name, Position, Age, Team) "
           "VALUES(%s, %s, %s, %s)"
           )
           
#Fill Player table with tuple from above
mycursor.executemany(sqlform1, player_tuple)

mydb.commit()

sqlform2 = (
           "INSERT INTO BeforeQ(Name, PTS, FGM, FGA, FGPercent, 3PM,"
           "3PA, 3PPercent, FTM, FTA, FTPercent, ORB, DRB, TRB, AST, TOV, STL, BLK, PF)" 
           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
           "%s, %s, %s, %s, %s, %s)"
          )

#Fill BeforeQ table with tuple from above
mycursor.executemany(sqlform2, beforeq_tuple)

mydb.commit()

#Close connections
mycursor.close()
mydb.close()

