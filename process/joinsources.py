#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:15:51 2018

@author: chrisstrods
"""

import pandas as pd
import organise as o
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import numpy
import difflib


def getMatchID(df):
    return (str(df["year"]) + str(o.getRoundCode(df["round"])) + \
            str(o.getTeamCode(df["hometeam"])) + \
            str(o.getTeamCode(df["awayteam"])))
    
def nameFormat(df,col):
    if(df[col] == "Western Bulldogs"):
        return "Footscray"
    elif(df[col] == "Kangaroos"):
        return "North Melbourne"
    elif(df[col] == "Brisbane"):
        return "Brisbane Lions"
    elif(df[col] == "GWS"):
        return "Greater Western Sydney"
    else:
        return df[col]

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(x["fullname"], 
                            choices=choices.loc[choices['matchid'] == x['matchid'], 
                                                'name'], 
                            scorer=scorer, 
                            score_cutoff=cutoff)[0]
    
#def nameChange(df):
#    if(df[col] == "X"):
#        return "Y"
#    elif(df[col] == "X"):
#        return "Y"
#    else:
#        return df[col]
        

def getPlayerMatchID(df):
    playerID = str(df["name"]).replace(" ","_")
    
    
    if(numpy.isnan(df["addcode"])):
        return str(playerID) + str(df["matchid"])
    else:
        return str(playerID) + str(df["matchid"]) + str(+ df["addcode"])


    

#load files    
summaries = pd.read_csv("../tables/match_summaries.csv")
player_stats = pd.read_csv("../tables/player_stats.csv")
extra_summaries = pd.read_csv("../extra_data/matchdetails.csv")
extra_player_stats = pd.read_csv("../extra_data/playerstats.csv")





extra_summaries["hometeam"] = extra_summaries.apply(nameFormat, col="hometeam", axis=1)
extra_summaries["awayteam"] = extra_summaries.apply(nameFormat, col="awayteam", axis=1)
extra_summaries["matchid"] = extra_summaries.apply(getMatchID, axis=1)
extra_summaries.rename(columns={'gameID_fw':'gameID'}, inplace=True)

player_stats["fullname"] = player_stats["first_name"] + " " +  \
    player_stats["last_name"]
        

player_stats_test = player_stats.head(100)
extra_players_test = extra_player_stats.head(100)
extra_summaries_test = extra_summaries.head(n=100)



extra_players_joined = pd.merge(extra_player_stats,extra_summaries,how="left",on="gameID")
extra_players_joined_trimmed = extra_players_joined[['name','homeAway','hometeam','awayteam','AFLfantasy','Supercoach','matchid']]
extra_players_joined_trimmed_test = extra_players_joined_trimmed.head(100)


extra_players_joined_trimmed.index = extra_players_joined_trimmed.index.map(lambda x: difflib.get_close_matches(x, df1.index)[0])


#extra_players_joined_trimmed_test["Fuzzy1"] = extra_players_joined_trimmed_test.apply(fuzzy_match,
#                                args=(player_stats,fuzz.ratio, 80),axis=0)


#fantasy_joined["playermatchid"] = fantasy_joined.apply(getPlayerMatchID, axis=1)


#fantasy_test = fantasy_joined.head(n=100)


#fantasy_joined.to_csv("../extra_data/fantasy_joined.csv",mode="w")



#summaries_joined = pd.merge(summaries,extra_summaries,how="left",on="matchid")
#players_joined = pd.merge(player_stats,fantasy_joined,how="left",on="playermatchid")


#fantasy_test = fantasy_joined.head(n=100)
#summaries_test = summaries_joined.head(n=100)
#players_test = players_joined.head(n=100)


#players_joined.to_csv("../extra_data/players_joined.csv",mode="w")


#fantasy_joined["matchid"] = fantasy_joined.apply(getMatchID,axis=1)


