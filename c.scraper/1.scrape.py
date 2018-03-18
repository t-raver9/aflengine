#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:31:18 2018

@author: chrisstrods
"""


import functions as f
import os, sys, numpy as np
from os.path import dirname, abspath
import re
import timeit



#Process and return match summary box
def getSummary(t):
    cells=list()
    for cell in t.findAll("td"):
        cells.append(cell.text)


    matchstring = str(cells[1]).split(" ")


    if(len(cells)==25): #Game finishing in regular time
        umpstring = str(cells[24]).split(",")
    elif(len(cells)==29): #Game finishing in overtime
        umpstring = str(cells[28]).split(",")
    else:
        umpstring = "ERROR"

    #If match is a final, remove 'FINAL' cell so that it aligns with
    #Round numbers
    if(str(matchstring[2]) == "Final"):
        del matchstring[2]


    #Create blank row to be filled
    outrow = [None] * 26
    outrow[0] = matchstring[1] #round


    if(len(matchstring) == 14): #Venue name two words
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","") #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[13] #venue
    elif(len(matchstring) == 13): #Venue name one word
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[12] #venue
    elif(len(matchstring) == 12): #Venue name two words, no crowd
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[11] #venue
    elif(len(matchstring) == 11): #Venue name one word, no crowd
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[10] #venue
    elif(len(matchstring) == 10): #Venue name two words, no venue or timezeone
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
    elif(len(matchstring) == 9): #Venue name one word, no venue or timezeone
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
    else:
        print ("Error with file:" + str(cells[1]) + "   " + str(len(matchstring)))

    outrow[25] = f.getMatchIndex(t)

    #Process teams and quarter by quarter scores for non overtime games
    if(len(cells)==25): #Game finishing in regular time
        outrow[6] = f.replaceTeam(cells[3])    #hteam
        outrow[7] = cells[4]    #hteamQ1
        outrow[8] = cells[5]    #hteamQ2
        outrow[9] = cells[6]    #hteamQ3
        outrow[10] = cells[7]   #hteamQ4
        outrow[11] = f.replaceTeam(cells[8])   #ateam
        outrow[12] = cells[9]   #ateamQ1
        outrow[13] = cells[10]  #ateamQ2
        outrow[14] = cells[11]  #ateamQ3
        outrow[15] = cells[12]  #ateamQ4
    elif(len(cells)==29): #Game finishing in overtime
        outrow[6] = f.replaceTeam(cells[3])    #hteam
        outrow[7] = cells[4]    #hteamQ1
        outrow[8] = cells[5]    #hteamQ2
        outrow[9] = cells[6]    #hteamQ3
        outrow[10] = cells[7]   #hteamQ4
        outrow[11] = f.replaceTeam(cells[8])   #ateam
        outrow[12] = cells[10]   #ateamQ1
        outrow[13] = cells[11]  #ateamQ2
        outrow[14] = cells[12]  #ateamQ3
        outrow[15] = cells[13]  #ateamQ4
        outrow[22] = cells[8]  #hteamET
        outrow[23] = cells[14]  #ateamET


    #Process differently based on howm any umpires in the game
    if(len(umpstring)>2):
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   umpstring[1].split("(")[0]#umpire2
        outrow[18] =   umpstring[2].split("(")[0]
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   re.sub("[^0-9]", "",str(umpstring[1]))
        outrow[21] =   re.sub("[^0-9]", "",str(umpstring[2]))
    elif(len(umpstring)>1):
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   umpstring[1].split("(")[0]#umpire2
        outrow[18] =   ""
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   re.sub("[^0-9]", "",str(umpstring[1]))
        outrow[21] =   ""
    else:
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   ""
        outrow[18] =   ""
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   ""
        outrow[21] =   ""
    return outrow




def getPlayerStats(p,t,ha,s):
    rows=list()
    for row in t.findAll("tr"):
        rows.append(row)

    if(len(rows) <22):
        print("FUCKED UP")
        print(t)
        print(len(rows))
    else:
        rowpoint = 2

        #loop through each player in team
        while(True):
            outrow = [None] * 30
            cells = list()
            for cell in rows[rowpoint].findAll("td"):
                cells.append(cell.text)

            if(cells[0] == "Rushed" or cells[0] == "Totals"):
                break;

            playerID = rows[rowpoint].find("a",href=True)['href'].split("/")[4].split(".")[0]
            team = rows[0].text.split(" Match")[0]

            outrow[0] = playerID
            outrow[1] = f.getMatchIndex(s)
            outrow[2] = f.replaceTeam(team)
            outrow[3] = ha
            outrow[4] = cells[1].split(",")[1]
            outrow[5] = cells[1].split(",")[0]
            outrow[6] = cells[0]
            outrow[7] = cells[2]
            outrow[8] = cells[3]
            outrow[9] = cells[4]
            outrow[10] = cells[5]
            outrow[11] = cells[6]
            outrow[12] = cells[7]
            outrow[13] = cells[8]
            outrow[14] = cells[9]
            outrow[15] = cells[10]
            outrow[16] = cells[11]
            outrow[17] = cells[12]
            outrow[18] = cells[13]
            outrow[19] = cells[14]
            outrow[20] = cells[15]
            outrow[21] = cells[16]
            outrow[22] = cells[17]
            outrow[23] = cells[18]
            outrow[24] = cells[19]
            outrow[25] = cells[20]
            outrow[26] = cells[21]
            outrow[27] = cells[22]
            outrow[28] = cells[23]
            outrow[29] = cells[24]
            p.loc[len(p)] = outrow
            rowpoint += 1
        return p



def scrape(syear,eyear):

    d = dirname(dirname(abspath(__file__)))
    startyear = syear
    endyear = eyear
    year = endyear
    summaries = f.initSummaries()
    player_stats = f.initPlayerStats()
    #scoring_progression = f.initScoringProgression()

    #iterate through each year, run the scraping process
    while(year>=startyear):
        print("Processing year: " + str(year))


        files = os.listdir(d + "/d.matchfiles/" + str(year))

        #Iterate through each match in the year
        i = 1
        for file in files:

            #Load the match HTML
            rawmatch = f.loadPage(d + "/d.matchfiles/" + str(year) + "/" + file)

            #removes the 'records' table if there is one
            if(len(rawmatch) == 9):
                del rawmatch[1]
            elif(len(rawmatch) == 8 and year <= 2007):
                del rawmatch[1]

            #Scrape the Match Summary
            summaries.loc[len(summaries)] = getSummary(rawmatch[0])
            summaries.fillna('')
            summaries = summaries.replace(np.nan, '', regex=True)

            #Scrape the player stats
            player_stats = getPlayerStats(player_stats,rawmatch[2],'H',rawmatch[0])
            player_stats = getPlayerStats(player_stats,rawmatch[4],'A',rawmatch[0])
            player_stats = player_stats.replace(np.nan, '', regex=True)
            
            


            #Scrape the scoring progression (if applicable)
            #TODO

        
            if(os.path.isfile("../d.input/match_summaries.csv")):
                summaries.to_csv("../d.input/match_summaries.csv", mode="a",header=False,index=False)
                player_stats.to_csv("../d.input/player_stats.csv", mode="a",header=False,index=False)
            else:
                summaries.to_csv("../d.input/match_summaries.csv", mode="w",index=False)
                player_stats.to_csv("../d.input/player_stats.csv", mode="w",index=False)
        
            summaries = f.initSummaries()
            player_stats = f.initPlayerStats()
            #print("Completed game #" + str(i) + " in season " + str(year))
            i += 1
        
        #else:
        #    summaries.to_csv("../d.input/match_summaries.csv", mode="a",header=False,index=False)
        #    player_stats.to_csv("../d.input/player_stats.csv", mode="a",header=False,index=False)
        year -= 1
        

    #player_stats["subbed"] = player_stats.apply(f.checkSub,axis=1)
    #player_stats["number"] = player_stats.apply(f.cleanNumber,axis=1)

    return summaries, player_stats





#If run from command line, takes year ranges as parameters, otherwise
#uses defaults
if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Using default season range of 1897 to 2017")
        syear = 1897
        eyear = 2017
    else:
        syear = int(sys.argv[1])
        eyear = int(sys.argv[2])

    summaries, players = scrape(syear,eyear)

    #Output to CSV
    #summaries.to_csv("../d.input/match_summaries.csv", mode="w")
    #players.to_csv("../d.input/player_stats.csv", mode="w")
