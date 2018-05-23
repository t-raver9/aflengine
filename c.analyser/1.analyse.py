#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:19:11 2018

@author: chrisstrods
"""

import pandas as pd
import afunctions as a

def calcPoints(hs):
    #calculate points scored per game
    hs["totalpoints"] = hs.apply(a.getPoints,axis=1)
    return hs


#group into average points per game per season and sort
def meanScoreSeason(hs):
    averages = hs.groupby('season')['totalpoints'].mean().sort_values(ascending=False)
    return averages


def getPoints(df):
    return int(df["hteam_q4"].split(".")[2]) + \
            int(df["ateam_q4"].split(".")[2])
            
def getAccuracy(df):
    goals = int(df["hteam_q4"].split(".")[0]) + \
        int(df["ateam_q4"].split(".")[0])
    
    behinds = int(df["hteam_q4"].split(".")[1]) + \
        int(df["ateam_q4"].split(".")[1])
    return (goals / (goals + behinds) * 100)


def getUmpireGames(df):
    games = df["umpire1games"] + df["umpire2games"] + df["umpire3games"]
    return games

def PannellCheck(df):
    if(df["umpire1"] == "Troy Pannell") or (df["umpire2"] == "Troy Pannell") or (df["umpire3"] == "Troy Pannell"):
        return "True"
    else:
        return "False"
    

def dogsPlaying(df):
    if(df["hteam"] == "Footscray") or (df["ateam"] == "Footscray"):
        return "True"
    else:
        return "False"
    
def dogPannelDiff(df):
    if(df["hteam"] == "Footscray"):
        return df["home_frees"] - df["away_frees"]
    else:
        return df["away_frees"] - df["home_frees"]


#Calculate score figures for grounds
def groundStats(hs):
    summaries2000 = hs.loc[hs['season'] >= 2000]
    summaries2000["totalpoints"] = summaries2000.apply(a.getPoints,axis=1)
    summaries2000["accuracy"] = summaries2000.apply(a.getAccuracy,axis=1)
    ground_score_averages = summaries2000.groupby('venue')['totalpoints'].mean().sort_values(ascending=False)
    ground_score_count = summaries2000.groupby('venue')['matchid'].count().sort_values(ascending=False)
    ground_score_accuracy = summaries2000.groupby('venue')['accuracy'].mean().sort_values(ascending=False)
    ground_data = pd.concat([ground_score_averages,ground_score_count,ground_score_accuracy],axis=1)
    ground_data = ground_data[ground_data.matchid >= 50]
    ground_data.rename(columns={'matchid': 'matches','totalpoints':'avepoints'}, inplace=True)
    return ground_data

####
###PROCESSING CODE
###

#load modern data (2010 onwards)
summaries = pd.read_csv("../d.output/modern_full_summaries.csv")
player_stats = pd.read_csv("../d.output/modern_full_players.csv")
hist_players = pd.read_csv("../d.output/historic_full_players.csv")
hist_summaries = pd.read_csv("../d.output/historic_full_summaries.csv")



#def umpireAnalysis(hs,ps):
summaries2000 = hist_summaries.loc[hist_summaries['season'] >= 2000]
summaries2000["umpexperience"] = summaries2000.apply(getUmpGames,axis=1)
    
players2000 = hist_players.loc[hist_players['year'] >= 2000]
players2000.rename(columns={'matchid_x': 'matchid'}, inplace=True)

pd.to_numeric(players2000["frees_against"])

freegames = players2000.groupby('matchid')['frees_against'].sum()
freegames2 = pd.merge(freegames,summaries2000,how="left",on="matchid")
    
#return freegames2


#umpstats = umpireAnalysis(hist_summaries,hist_players)

