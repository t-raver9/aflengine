#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:31:18 2018

@author: chrisstrods
"""


import scrapefunctions as f
import os
import sys
from os.path import dirname, abspath


def scrape(syear,eyear):


    d = dirname(dirname(abspath(__file__)))
    startyear = syear
    endyear = eyear
    year = endyear
    match_summaries = f.initSummaries()
    player_stats = f.initPlayerStats()
    #scoring_progression = f.initScoringProgression()
    
    #iterate through each year, run the scraping process
    while(int(year)>=int(startyear)):
        print("Processing year: " + str(year))
        
        
        files = os.listdir(d + "/matchfiles/" + str(year))
        
        #Iterate through each match in the year
        for file in files:
            
            #Load the match HTML
            rawmatch = f.loadPage(d + "/matchfiles/" + str(year) + "/" + file)
            
            #removes the 'records' table if there is one
            if(len(rawmatch) == 9):
                del rawmatch[1]
            elif(len(rawmatch) == 8 and int(year) <= 2007):
                del rawmatch[1]
            
            #Scrape the Match Summary
            match_summaries.loc[len(match_summaries)] = f.getSummary(rawmatch[0])
            
            #Scrape the player stats
            player_stats = f.getPlayerStats(player_stats,rawmatch[2],'H',rawmatch[0])
            player_stats = f.getPlayerStats(player_stats,rawmatch[4],'A',rawmatch[0])
            
            #Scrape the scoring progression (if applicable)
            #TODO
            
        year -= 1
            

    #return match_summaries, player_stats
    return player_stats
    
    

         
            
#If run from command line, takes year ranges as parameters, otherwise
#uses defaults
if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Using default season range of 1897 to 2017")
        syear = 2017
        eyear = 2017
    else:
        syear = int(sys.argv[1])
        eyear = int(sys.argv[2])
    
    #summaries, players = scrape(syear,eyear)
    players=scrape(syear,eyear)
    
    
    #Output to CSV
    #summaries.to_csv("../outputs/match_summaries.csv", mode="w")
    #players.to_csv("../outputs/player_stats.csv", mode="w")   








#rawmatch = f.loadPage(folder)
#match_summary= match[0]
#home_stats= match[2]
#away_stats= match[4]
#home_details= match[5]
#away_details= match[6]
#score_progression= match[7]






