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

<<<<<<< HEAD


=======
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
odds["hometeam"] = odds.apply(f.nameFormat, col="hometeam", axis=1)
odds["awayteam"] = odds.apply(f.nameFormat, col="awayteam", axis=1)
odds["year"] = odds.apply(f.getYear, axis=1)
odds["matchid"] = odds.apply(f.getMatchID, axis=1)

fantasy = pd.merge(fantasy,odds,how="left",on="gameID")
<<<<<<< HEAD
fantasy.drop(["gameID"], axis=1, inplace=True)
=======
fantasy.drop(["Unnamed: 0_x", "gameID","Unnamed: 0_y"], axis=1, inplace=True)
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85


fantasy["fullname"] = fantasy.apply(f.nameClean,axis=1)

fantasy["namekey"] = fantasy.apply(f.getNameKeyFW,axis=1)

player_stats["namekey"] = player_stats.apply(f.getNameKeyAT,axis=1)



<<<<<<< HEAD
=======

>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
fantasy["fullkey"] = fantasy.apply(f.getFullKey,axis=1)
player_stats["fullkey"] = player_stats.apply(f.getFullKey,axis=1)


full_summaries = pd.merge(summaries,odds,how="left",on="matchid")


<<<<<<< HEAD


player_full = pd.merge(player_stats,fantasy,how="left",on="fullkey")
player_full["year"] = player_full.apply(f.fillYear,axis=1)

modern_full_P = player_full.loc[player_full["year"] >= 2010]
modern_full_M = full_summaries.loc[full_summaries["year"] >= 2010]

modern_full_P.to_csv("../d.output/modern_full_players.csv", mode="w", index=False)
player_full.to_csv("../d.output/historic_full_players.csv", mode="w", index=False)
full_summaries.to_csv("../d.output/historic_full_summaries.csv", mode="w", index=False)
fantasy.to_csv("../d.output/fantasy_full.csv", mode="w", index=False)
=======
player_full = pd.merge(player_stats,fantasy,how="left",on="fullkey")
player_full["year"] = player_full.apply(f.fillYear,axis=1)

#head_full = player_full.head(n=100)

modern_full = player_full.loc[player_full["year"] >= 2010]


modern_full.to_csv("../d.input/modern_full_players.csv", mode="w")

fantasy.to_csv("../d.input/fantasy_full.csv", mode="w")

full_summaries.to_csv("../d.input/modern_full_summaries.csv", mode="w")

#player_stats.to_csv("../d.input/player_stats.csv", mode="w")

#extra_summaries.rename(columns={'gameID_fw':'gameID'}, inplace=True)
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
