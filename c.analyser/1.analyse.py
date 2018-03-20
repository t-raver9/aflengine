#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:19:11 2018

@author: chrisstrods
"""

import pandas as pd
import afunctions as a

#load modern data (2010 onwards)
summaries = pd.read_csv("../d.output/modern_match_summaries.csv")
player_stats = pd.read_csv("../d.output/modern_full_players.csv")

#load historical match summaries
hist_summaries = pd.read_csv("../d.output/historic_match_summaries.csv")

#calculate points scored per game
hist_summaries["totalpoints"] = hist_summaries.apply(a.getPoints,axis=1)

#group into average points per game per season and sort
average_scores = hist_summaries.groupby('season')['totalpoints'].mean().sort_values(ascending=False)


average_scores.to_csv("../d.analysis/points_per_game.csv", mode="w")


