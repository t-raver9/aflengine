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

<<<<<<< HEAD

#load historial data
hsummaries = pd.read_csv("../d.output/historic_match_summaries.csv")
hplayer_stats = pd.read_csv("../d.output/historic_full_players.csv")


#GROUP POINTS PER SEASON
=======
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
#load historical match summaries
hist_summaries = pd.read_csv("../d.output/historic_match_summaries.csv")

#calculate points scored per game
hist_summaries["totalpoints"] = hist_summaries.apply(a.getPoints,axis=1)

#group into average points per game per season and sort
average_scores = hist_summaries.groupby('season')['totalpoints'].mean().sort_values(ascending=False)


<<<<<<< HEAD

#GROUP SCORES BY GROUND
summaries2000 = hsummaries.loc[hsummaries['season'] >= 2000]
summaries2000["totalpoints"] = summaries2000.apply(a.getPoints,axis=1)
summaries2000["accuracy"] = summaries2000.apply(a.getAccuracy,axis=1)
ground_score_averages = summaries2000.groupby('venue')['totalpoints'].mean().sort_values(ascending=False)
ground_score_count = summaries2000.groupby('venue')['matchid'].count().sort_values(ascending=False)
ground_score_accuracy = summaries2000.groupby('venue')['accuracy'].mean().sort_values(ascending=False)
ground_data = pd.concat([ground_score_averages,ground_score_count,ground_score_accuracy],axis=1)
ground_data = ground_data[ground_data.matchid >= 50]

ground_data.rename(columns={'matchid': 'matches','totalpoints':'avepoints'}, inplace=True)
=======
average_scores.to_csv("../d.analysis/points_per_game.csv", mode="w")


>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
