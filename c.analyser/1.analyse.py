#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:19:11 2018

@author: chrisstrods
"""

import pandas as pd
import afunctions as a

#load modern data (2010 onwards)
summaries = pd.read_csv("../d.output/modern_full_summaries.csv")
player_stats = pd.read_csv("../d.output/modern_full_players.csv")
hist_players = pd.read_csv("../d.output/historic_full_players.csv")
hist_summaries = pd.read_csv("../d.output/historic_full_summaries.csv")

def calcPoints(hs):
    #calculate points scored per game
    hs["totalpoints"] = hs.apply(a.getPoints,axis=1)
    return hs


#group into average points per game per season and sort
def meanScoreSeason(hs):
    averages = hs.groupby('season')['totalpoints'].mean().sort_values(ascending=False)
    return averages


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

#def umpireAnalysis(hs,ps):
summaries2000 = hist_summaries.loc[hist_summaries['season'] >= 2000]
summaries2000["umpexperience"] = summaries2000.apply(a.getUmpGames,axis=1)
    
players2000 = hist_players.loc[hist_players['year'] >= 2000]
players2000.rename(columns={'matchid_x': 'matchid'}, inplace=True)

pd.to_numeric(players2000["frees_against"])

freegames = players2000.groupby('matchid')['frees_against'].sum()
freegames2 = pd.merge(freegames,summaries2000,how="left",on="matchid")
    
#return freegames2


#umpstats = umpireAnalysis(hist_summaries,hist_players)

