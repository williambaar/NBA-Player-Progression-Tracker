# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 19:39:41 2020

@author: William Baar

This program will:
    1. Utilize the Selenium package to web scrape NBA player 
       statistics from NBA.com. (Note. a specific date range will be specified so that 
       AfterQ table only scrapes stats from after quarantine. This feature was not available
       on BasketballReference.com).
    2. Store the data into two lists of tuples for easier entry into a MySQL database.
    3. Connect to the MySQL Database server and update the data in AfterQ table as games are played.
    4. This Python script will be automated to run every 24 hours. 
"""

#Packages for webscraping data
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#Package for connecting to the MySQL Database server
import mysql.connector

driver = webdriver.Chrome(ChromeDriverManager().install())

#Connect to NBA.com/Stats website URL
url = "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1&Season=2019-20&SeasonType=Regular%20Season&DateFrom=07%2F30%2F2020"
driver.get(url)

driver.implicitly_wait(5)

#Create an ActionChains object.
#This will be used to navigate the webpage.
actions = ActionChains(driver)

"""
On NBA.com, the statistics are spread out over multiple pages.
Therefore, we must tell Selenium to select the drop down 
box and change format from page 1 to "All" pages.
"""

#row is the location of the row containing the drop down box
row = driver.find_element_by_class_name("stats-table-pagination__info")

#dropdown is the drop down box
dropdown = row.find_element_by_tag_name("select")

#option is the "All" option, which happens to be the first on the list
option = dropdown.find_element_by_tag_name("option")


#Once the page loads, the drop down box is covered by a pop-up.
#Therefore, we must scroll down to make it visible.
driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
driver.implicitly_wait(3) 

#Using the ActionChains object, navigate to the drop down box and select "All"
actions.move_to_element(dropdown)
actions.click(dropdown)
actions.send_keys(Keys.ARROW_UP)
actions.send_keys(Keys.RETURN)
actions.perform()


#table is the entire dataset
table = driver.find_element_by_tag_name("table")

#rows is each row of statistics in the table
rows = table.find_elements_by_tag_name("tr")

#list_container will be a list of lists containing all player statistics
list_container = list()

#Each row contains a player, his rank (ID), and statistics like PPG, APG, RPG, etc.
#Parse all this information and store it in a list
for player in rows:
    
    each = list()
    
    for stat in player.find_elements_by_tag_name("td"): #Each players statistics
        
        print(stat.text)
        
        each.append(stat.text)
    
    list_container.append(each)

#The first list in the container is the different stat categories,
#so we can delete this.
del list_container[0]

driver.close()

#Create a new tuple_container that holds all AfterQ table information
afterq_table = list()
for column in list_container:
    each = list()
    each.append(column[1])
    each.append(column[8])
    each.append(column[9])
    each.append(column[10])
    each.append(column[11])
    each.append(column[12])
    each.append(column[13])
    each.append(column[14])
    each.append(column[15])
    each.append(column[16])
    each.append(column[17])
    each.append(column[18])
    each.append(column[19])
    each.append(column[20])
    each.append(column[21])
    each.append(column[22])
    each.append(column[23])
    each.append(column[24])
    each.append(column[25])
    afterq_table.append(each)
    
#Convert list of lists to list of tuples for easier entry into MySQL database
afterq_tuple = [tuple(l) for l in afterq_table]

 #---------------------------------------------------------------------------------------
 
#Connect to MySQL connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="####", database="NBA_Player_Stats")

mycursor = mydb.cursor()

#Update player statistics by clearing AfterQ table and inserting new data as games are played
mycursor.execute(
                "TRUNCATE TABLE AfterQ"
                )
          
sqlform3 = (
           "INSERT INTO AfterQ(Name, PTS, FGM, FGA, FGPercent, 3PM,"
           "3PA, 3PPercent, FTM, FTA, FTPercent, ORB, DRB, TRB, AST, TOV, STL, BLK, PF)" 
           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
           "%s, %s, %s, %s, %s, %s)"
          )

#Fill AfterQ table with tuple from above
mycursor.executemany(sqlform3, afterq_tuple)

mydb.commit()

#Close connections
mycursor.close()
mydb.close()
    
