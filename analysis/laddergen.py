#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:03:08 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath


def getLadder(df):
    
    #Create a ladder table
    ladder = []
    teams = df.hteam.unique().tolist()
    for team in teams:
        ladder.append({'team':team,'played':0,'wins':0,'losses':0,\
                       'draws':0, 'for':0,'against':0,'percentage':0,\
                       'points':0})    
    ladder = pd.DataFrame.from_dict(ladder)
    ladder.set_index('team',inplace=True)
    
    #Calc ladder
    
    for index, match in df.iterrows():
        #Don't process if it's a final
        if(match["round"].isdigit() == False):
            continue
        
        
        #Increment game counts
        ladder.loc[match["hteam"]]["played"] +=1
        ladder.loc[match["ateam"]]["played"] +=1
        
        #Increment scores
        ladder.loc[match["hteam"]]["for"] += match["hscore"]
        ladder.loc[match["hteam"]]["against"] += match["ascore"]
        ladder.loc[match["ateam"]]["for"] += match["ascore"]
        ladder.loc[match["ateam"]]["against"] += match["hscore"]
        
        #Process draw
        if(match["hscore"] == match["ascore"]):
            ladder.loc[match["hteam"]]["draws"] +=1
            ladder.loc[match["ateam"]]["draws"] +=1
        elif(match["hscore"] > match["ascore"]):
            ladder.loc[match["hteam"]]["wins"] +=1
            ladder.loc[match["ateam"]]["losses"] +=1
        else:
            ladder.loc[match["ateam"]]["wins"] +=1   
            ladder.loc[match["hteam"]]["losses"] +=1    
    
    
    ladder["points"] = (ladder["wins"] * 4) + (ladder["draws"] * 2)
    ladder["percentage"] = (ladder["for"] / ladder["against"]) * 100
          
    ladder.sort_values(["points","percentage"],ascending=False,\
                       inplace=True)
    
    ladder = ladder [["played","wins","draws","losses","for",\
                      "against","percentage","points"]]
    
    return ladder



def getInterstateLadder(df,gloc,tloc):
    
    #Create a ladder table
    ladder = []
    teams = df.hteam.unique().tolist()
    for team in teams:
        ladder.append({'team':team,'played':0,'wins':0,'losses':0,\
                       'draws':0, 'for':0,'against':0,'percentage':0,\
                       'points':0})    
    ladder = pd.DataFrame.from_dict(ladder)
    ladder.set_index('team',inplace=True)
    
    #Calc ladder        
    df = df.merge(gloc,how="left",right_on="Venue",left_on="venue")
    df.rename(columns={'State':'matchstate'}, inplace=True)
    df.drop(columns=["Venue"], inplace=True)

    df = df.merge(tloc,how="left",right_on="Team",left_on="hteam")
    df.rename(columns={'State':'homestate'}, inplace=True)
    df.drop(columns=["Team"], inplace=True)
    
    df = df.merge(tloc,how="left",right_on="Team",left_on="ateam")
    df.rename(columns={'State':'awaystate'}, inplace=True)
    df.drop(columns=["Team"], inplace=True)    
    
    for index, match in df.iterrows():
        #Don't process if it's a final
        if(match["round"].isdigit() == False):
            continue
        
        
        #if home team out of state, process
        if(match["matchstate"] != match["homestate"]):
            #Increment game counts
            ladder.loc[match["hteam"]]["played"] +=1            
            #Increment scores
            ladder.loc[match["hteam"]]["for"] += match["hscore"]
            ladder.loc[match["hteam"]]["against"] += match["ascore"]            
            #Process draw
            if(match["hscore"] == match["ascore"]):
                ladder.loc[match["hteam"]]["draws"] +=1
            elif(match["hscore"] > match["ascore"]):
                ladder.loc[match["hteam"]]["wins"] +=1
            else:
                ladder.loc[match["hteam"]]["losses"] +=1        
        

        #if away team out of state, process
        if(match["matchstate"] != match["awaystate"]):

            #Increment game counts
            ladder.loc[match["ateam"]]["played"] +=1
            
            #Increment scores
            ladder.loc[match["ateam"]]["for"] += match["ascore"]
            ladder.loc[match["ateam"]]["against"] += match["hscore"]
            
            #Process draw
            if(match["hscore"] == match["ascore"]):
                ladder.loc[match["ateam"]]["draws"] +=1
            elif(match["hscore"] > match["ascore"]):
                ladder.loc[match["ateam"]]["losses"] +=1
            else:
                ladder.loc[match["ateam"]]["wins"] +=1   

    
    
    ladder["points"] = (ladder["wins"] * 4) + (ladder["draws"] * 2)
    ladder["percentage"] = (ladder["for"] / ladder["against"]) * 100
    ladder["winpercent"] = (ladder["wins"] / ladder["played"] * 100)
          
    ladder.sort_values(["winpercent","percentage"],ascending=False,\
                       inplace=True)
    
    ladder = ladder [["played","wins","draws","losses","for",\
                      "against","percentage","points","winpercent"]]
    
    return ladder








#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
gloc = pd.read_csv(d+"/bench/extras/ground_locations.csv")
tloc = pd.read_csv(d+"/bench/extras/team_locations.csv")

curr_season = matches.loc[(matches["season"]==2018)]

current_ladder = getLadder(curr_season)
interstate_ladder = getInterstateLadder(curr_season,gloc,tloc)


current_ladder.to_csv(d+"/outputs/ladder2018.csv")
interstate_ladder.to_csv(d+"/outputs/interstateladder2018.csv")





