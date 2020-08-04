# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:08:49 2020

@author: William Baar

This program will:
    1. Connect to the MySQL database server.
    2. Create three different tables under the Nba_Player_Stats database:
       Player, BeforeQ and AfterQ.
"""

import mysql.connector

#Connect to MySQL connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="####", database="NBA_Player_Stats")

mycursor = mydb.cursor()
 
#Create table that holds all player information
#Each NBA player has a unique name. This will serve as the primary key.
mycursor.execute(
                "CREATE TABLE IF NOT EXISTS Player(Name VARCHAR(30) PRIMARY KEY,"
                "Position VARCHAR(5), Age SMALLINT UNSIGNED, Team VARCHAR(3))"
                )
  
#Create a table that holds all player statistics prior to quarantine
mycursor.execute(
                 "CREATE TABLE IF NOT EXISTS BeforeQ(Name VARCHAR(30) PRIMARY KEY," 
                 "FOREIGN KEY(Name) REFERENCES Player(Name), PTS FLOAT, FGM FLOAT,"
                 "FGA FLOAT, FGPercent FLOAT, 3PM FLOAT, 3PA FLOAT,"
                 "3PPercent FLOAT, FTM FLOAT, FTA FLOAT, FTPercent FLOAT,"
                 "ORB FLOAT, DRB FLOAT, TRB FLOAT, AST FLOAT, TOV FLOAT,"
                 "STL FLOAT, BLK FLOAT, PF FLOAT)"
                )
           
#Create a table that holds all player statistics after quarantine
mycursor.execute(
                 "CREATE TABLE IF NOT EXISTS AfterQ(Name VARCHAR(30) PRIMARY KEY,"
                 "FOREIGN KEY(Name) REFERENCES Player(Name), PTS FLOAT, FGM FLOAT,"
                 "FGA FLOAT, FGPercent FLOAT, 3PM FLOAT, 3PA FLOAT,"
                 "3PPercent FLOAT, FTM FLOAT, FTA FLOAT, FTPercent FLOAT,"
                 "ORB FLOAT, DRB FLOAT, TRB FLOAT, AST FLOAT, TOV FLOAT,"
                 "STL FLOAT, BLK FLOAT, PF FLOAT)"
                )
                 
#Close connections
mycursor.close()
mydb.close()
