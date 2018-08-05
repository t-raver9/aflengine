#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:03:08 2018

@author: chrisstrods
"""

import pandas as pd
import numpy as np
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
        
        if(np.isnan(match["hscore"])):
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



def getHalftimeLadder(df):
    
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

        home_ht = int(match["hteam_q2"].split(".")[2])
        away_ht = int(match["ateam_q2"].split(".")[2])      
        
        #Increment game counts
        ladder.loc[match["hteam"]]["played"] +=1
        ladder.loc[match["ateam"]]["played"] +=1
        
        #Increment scores
        ladder.loc[match["hteam"]]["for"] += home_ht
        ladder.loc[match["hteam"]]["against"] += away_ht
        ladder.loc[match["ateam"]]["for"] += away_ht
        ladder.loc[match["ateam"]]["against"] += home_ht
        
        #Process draw
        if(home_ht == away_ht):
            ladder.loc[match["hteam"]]["draws"] +=1
            ladder.loc[match["ateam"]]["draws"] +=1
        elif(home_ht > away_ht):
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



def getSecondhalfLadder(df):
    
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

        home_h2 = match["hscore"]-int(match["hteam_q2"].split(".")[2])
        away_h2 = match["ascore"]-int(match["ateam_q2"].split(".")[2])      
        
        #Increment game counts
        ladder.loc[match["hteam"]]["played"] +=1
        ladder.loc[match["ateam"]]["played"] +=1
        
        #Increment scores
        ladder.loc[match["hteam"]]["for"] += home_h2
        ladder.loc[match["hteam"]]["against"] += away_h2
        ladder.loc[match["ateam"]]["for"] += away_h2
        ladder.loc[match["ateam"]]["against"] += home_h2
        
        #Process draw
        if(home_h2 == away_h2):
            ladder.loc[match["hteam"]]["draws"] +=1
            ladder.loc[match["ateam"]]["draws"] +=1
        elif(home_h2 > away_h2):
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


def getFlippedLadder(df):
    
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
        
        
        if(abs(match["hscore"] - match["ascore"])<6):
            hscore = match["ascore"]
            ascore = match["hscore"]

        else:
            hscore = match["hscore"]
            ascore = match["ascore"]


        #Increment scores
        ladder.loc[match["hteam"]]["for"] += hscore
        ladder.loc[match["hteam"]]["against"] += ascore
        ladder.loc[match["ateam"]]["for"] += ascore
        ladder.loc[match["ateam"]]["against"] += hscore
        
        #Increment game counts
        ladder.loc[match["hteam"]]["played"] +=1
        ladder.loc[match["ateam"]]["played"] +=1
        

        
        #Process draw
        if(hscore == ascore):
            ladder.loc[match["hteam"]]["draws"] +=1
            ladder.loc[match["ateam"]]["draws"] +=1
        elif(hscore > ascore):
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




#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
gloc = pd.read_csv(d+"/bench/extras/ground_locations.csv")
tloc = pd.read_csv(d+"/bench/extras/team_locations.csv")

curr_season = matches.loc[(matches["season"]==2018)]

current_ladder = getLadder(curr_season)
interstate_ladder = getInterstateLadder(curr_season,gloc,tloc)
halftime_ladder = getHalftimeLadder(curr_season)
secondhalf_ladder = getSecondhalfLadder(curr_season)
flipped_ladder = getFlippedLadder(curr_season)

current_ladder.to_csv(d+"/outputs/ladder2018.csv")
interstate_ladder.to_csv(d+"/outputs/interstateladder2018.csv")
halftime_ladder.to_csv(d+"/outputs/halftimeladder2018.csv")
secondhalf_ladder.to_csv(d+"/outputs/secondhalfladder2018.csv")
flipped_ladder.to_csv(d+"/outputs/flippedladder2018.csv")


