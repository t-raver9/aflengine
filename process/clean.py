#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:18:09 2018

@author: chrisstrods
"""

import pandas as pd

#get rid of junk characters created when player is subbed on or off
def cleanNumber(df):
    if(len(str(df["number"])) > 2):
        return df["number"][:2]
    else:
        return df["number"]
    
#checks if a player was subbed on or off an creates a column for it 
def checkSub(df):
    if(len(str(df["number"])) > 2):
        if("↓" in str(df["number"])):
            return "off"
        elif("↑" in str(df["number"])):
            return "on"
        else:
            return ""
    else:
        return ""
    
 

    
    
    
#load files
summaries = pd.DataFrame.from_csv("../outputs/match_summaries.csv")
player_stats = pd.DataFrame.from_csv("../outputs/player_stats.csv")

#add sub and fix numbers
player_stats["subbed"] = player_stats.apply(checkSub,axis=1)
player_stats["number"] = player_stats.apply(cleanNumber,axis=1)





#save files
summaries.to_csv("../outputs/match_summaries_index.csv",mode="w")
player_stats.to_csv("../outputs/player_stats_index.csv",mode="w")