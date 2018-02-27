#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:31:18 2018

@author: chrisstrods
"""


import scrapefunctions as f
import os
import sys
import numpy as np
import time
from os.path import dirname, abspath



def scrape(syear,eyear):


    d = dirname(dirname(abspath(__file__)))
    startyear = syear
    endyear = eyear
    year = endyear
    summaries = f.initSummaries()
    player_stats = f.initPlayerStats()
    #scoring_progression = f.initScoringProgression()
    stamp = int(time.time())

    #iterate through each year, run the scraping process
    while(year>=startyear):
        print("Processing year: " + str(year))


        files = os.listdir(d + "/matchfiles/" + str(year))

        #Iterate through each match in the year
        for file in files:

            #Load the match HTML
            rawmatch = f.loadPage(d + "/matchfiles/" + str(year) + "/" + file)

            #removes the 'records' table if there is one
            if(len(rawmatch) == 9):
                del rawmatch[1]
            elif(len(rawmatch) == 8 and year <= 2007):
                del rawmatch[1]

            #Scrape the Match Summary
            summaries.loc[len(summaries)] = f.getSummary(rawmatch[0])
            summaries.fillna('')
            summaries = summaries.replace(np.nan, '', regex=True)
            

            #Scrape the player stats
            player_stats = f.getPlayerStats(player_stats,rawmatch[2],'H',rawmatch[0])
            player_stats = f.getPlayerStats(player_stats,rawmatch[4],'A',rawmatch[0])
            player_stats = player_stats.replace(np.nan, '', regex=True)
            
            
            #Scrape the scoring progression (if applicable)
            #TODO
            
        if(year==endyear):
            summaries.to_csv("../outputs/match_summaries" + str(stamp) +".csv", mode="w",index=False)
            player_stats.to_csv("../outputs/player_stats" + str(stamp) +".csv", mode="w",index=False)
        else:
            summaries.to_csv("../outputs/match_summaries" + str(stamp) +".csv", mode="a",header=False,index=False)
            player_stats.to_csv("../outputs/player_stats" + str(stamp) +".csv", mode="a",header=False,index=False)
        year -= 1
        summaries = f.initSummaries()
        player_stats = f.initPlayerStats()


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

    #summaries, players = scrape(syear,eyear)
    summaries, players=scrape(syear,eyear)


    #Output to CSV
    #summaries.to_csv("../outputs/match_summaries.csv", mode="a")
    #players.to_csv("../outputs/player_stats.csv", mode="a")








#rawmatch = f.loadPage(folder)
#match_summary= match[0]
#home_stats= match[2]
#away_stats= match[4]
#home_details= match[5]
#away_details= match[6]
#score_progression= match[7]






