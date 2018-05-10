#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 19:46:37 2018

@author: chrisstrods
"""


from pydata import libs #load tidyverse
from os.path import dirname, abspath
import afunctions as af
from scipy.stats.stats import pearsonr, spearmanr

globals().update(libs())


#load match and player data
d = dirname(dirname(abspath('__file__')))
players = pd.read_csv(d + "/d.output/players.csv")
matches = pd.read_csv(d + "/d.output/matches.csv")
p_mini = players.head(10)
m_mini = matches.head(10)

#Trim match data to only include 1990 onwards
mod_players = players.loc[players['season'] >= 1994]
mod_matches = matches.loc[matches['season'] >= 1994]


#Count frees paid per game and append them to the matches
home_players = mod_players.loc[mod_players["homeAway"] == "Home"]
away_players = mod_players.loc[mod_players["homeAway"] == "Away"]
frees = mod_players.groupby('matchid')['frees_for'].sum()
hfrees= home_players.groupby('matchid')['frees_for'].sum()
afrees= away_players.groupby('matchid')['frees_for'].sum()



#Calculate umpire games
matches_with_frees = mod_matches.merge(frees.to_frame(),  \
    left_on="matchid", right_index=True)

#Calc home away frees individually 
matches_with_frees = matches_with_frees.merge(hfrees.to_frame(),  \
    left_on="matchid", right_index=True)

matches_with_frees = matches_with_frees.merge(afrees.to_frame(),  \
    left_on="matchid", right_index=True)

matches_with_frees.rename(columns = {"frees_for_x":"total_frees", \
    "frees_for_y":"home_frees","frees_for":"away_frees"},inplace=True)



matches_with_frees["umpgames"] =  \
    matches_with_frees.apply(af.getUmpireGames,axis=1)

#Put umpgames and frees into standalone lists    
umpgames = matches_with_frees["umpgames"].tolist()
frees = matches_with_frees["frees_for"].tolist()




#PANNELL ANALYSIS
matches_with_frees["Pannell"] = matches_with_frees.apply(af.PannellCheck,axis=1)
matches_with_frees["Dogsplay"] = matches_with_frees.apply(af.dogsPlaying,axis=1)
dogpannell = matches_with_frees.loc[(matches_with_frees["Pannell"]=="True") & (matches_with_frees["Dogsplay"]=="True")]
dogpannell["freedifference"] = dogpannell.apply(af.dogPannelDiff,axis=1)
diff = dogpannell["freedifference"].sum()
avediff = dogpannell["freedifference"].mean()
dognopannell= matches_with_frees.loc[(matches_with_frees["Pannell"]=="False") & (matches_with_frees["Dogsplay"]=="True")]
dognopannell = dognopannell.loc[dognopannell["season"]>= 2010]
dognopannell["freedifference"] = dognopannell.apply(af.dogPannelDiff,axis=1)
revdiff = dognopannell["freedifference"].sum()
revavediff = dognopannell["freedifference"].mean()