#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 20:30:04 2018

@author: chrisstrods
"""

import pandas as pd
import functions as f

#load files    
summaries = pd.read_csv("../d.input/match_summaries.csv")
player_stats = pd.read_csv("../d.input/player_stats.csv")
odds = pd.read_csv("../d.input/odds_data.csv")
fantasy = pd.read_csv("../d.input/fantasy_scores.csv")

odds["hometeam"] = odds.apply(f.nameFormat, col="hometeam", axis=1)
odds["awayteam"] = odds.apply(f.nameFormat, col="awayteam", axis=1)
odds["year"] = odds.apply(f.getYear, axis=1)
odds["matchid"] = odds.apply(f.getMatchID, axis=1)

fantasy = pd.merge(fantasy,odds,how="left",on="gameID")
fantasy.drop(["Unnamed: 0_x", "gameID","Unnamed: 0_y"], axis=1, inplace=True)

fantasy["namekey"] = fantasy.apply(f.getNameKeyFW,axis=1)

player_stats["namekey"] = player_stats.apply(f.getNameKeyAT,axis=1)


fantasy["fullname"] = fantasy.apply(f.nameClean,axis=1)


fantasy["fullkey"] = fantasy.apply(f.getFullKey,axis=1)
player_stats["fullkey"] = player_stats.apply(f.getFullKey,axis=1)


head_player_stats = player_stats.head(100)
head_fantasy = fantasy.head(100)
head_summaries = summaries.head(n=100)


player_full = pd.merge(player_stats,fantasy,how="left",on="fullkey")

player_full["year"] = player_full.apply(f.fillYear,axis=1)

head_full = player_full.head(n=100)

modern_full = player_full.loc[player_full["year"] >= 2010]


modern_full.to_csv("../d.input/modern_full_players.csv", mode="w")

fantasy.to_csv("../d.input/fantasy_full.csv", mode="w")

player_stats.to_csv("../d.input/player_stats.csv", mode="w")

#extra_summaries.rename(columns={'gameID_fw':'gameID'}, inplace=True)