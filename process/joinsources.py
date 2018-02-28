#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:15:51 2018

@author: chrisstrods
"""

import pandas as pd
import organise as o


def getMatchID(df):
    return (str(df["year"]) + str(o.getRoundCode(df["round"])) + \
            str(o.getTeamCode(df["hometeam"])) + \
            str(o.getTeamCode(df["awayteam"])))


#load files
summaries = pd.DataFrame.from_csv("../outputs/match_summaries_index.csv")
player_stats = pd.DataFrame.from_csv("../outputs/player_stats_index.csv")
betting_stats = pd.DataFrame.from_csv("../extra_data/odds.csv")
fantasy_player_stats = pd.DataFrame.from_csv("../extra_data/fantplayerstats.csv")
fantasy_match_details = pd.DataFrame.from_csv("../extra_data/fantmatchdetails.csv")

fantasy_player_stats["gameID"] = pd.to_numeric(fantasy_player_stats["gameID"])

fantasy_joined = pd.merge(fantasy_player_stats,fantasy_match_details,how="left",on="gameID")



fantasy_joined['awayteam'].replace(to_replace="Western Bulldogs",
    value="Footscray",inplace=True)
fantasy_joined['hometeam'].replace(to_replace="Western Bulldogs",
    value="Footscray",inplace=True)
fantasy_joined['awayteam'].replace(to_replace="Kangaroos",
    value="Footscray",inplace=True)
fantasy_joined['hometeam'].replace(to_replace="Kangaroos",
    value="North Melbourne",inplace=True)
fantasy_joined['awayteam'].replace(to_replace="Brisbane",
    value="Brisbane Lions",inplace=True)
fantasy_joined['hometeam'].replace(to_replace="Brisbane",
    value="Brisbane Lions",inplace=True)
fantasy_joined['hometeam'].replace(to_replace="GWS",
    value="Greater Western Sydney",inplace=True)
fantasy_joined['awayteam'].replace(to_replace="GWS",
    value="Greater Western Sydney",inplace=True)


fantasy_joined["matchid"] = fantasy_joined.apply(getMatchID,axis=1)


