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

#Drop any games which have been scraped twice
odds.drop_duplicates(subset="gameID",inplace=True)
summaries.drop_duplicates(subset="matchid",inplace=True)

#Generate columns for odds file
odds["hometeam"] = odds.apply(f.nameFormat, col="hometeam", axis=1)
odds["awayteam"] = odds.apply(f.nameFormat, col="awayteam", axis=1)
odds["year"] = odds.apply(f.getYear, axis=1)
odds["matchid"] = odds.apply(f.getMatchID, axis=1)

#Merge fantasy with odds to get match details
fantasy = pd.merge(fantasy,odds,how="left",on="gameID")
fantasy.drop(["gameID"], axis=1, inplace=True)

#Generate merge columns to get join key for fantasy file
fantasy["fullname"] = fantasy.apply(f.nameClean,axis=1)
fantasy["namekey"] = fantasy.apply(f.getNameKeyFW,axis=1)
fantasy["fullkey"] = fantasy.apply(f.getFullKey,axis=1)

#Generate merge columns to get join key for player stats file
player_stats["namekey"] = player_stats.apply(f.getNameKeyAT,axis=1)
player_stats["fullkey"] = player_stats.apply(f.getFullKey,axis=1)

#Join match summaries with odds file to get all match data
full_summaries = pd.merge(summaries,odds,how="left",on="matchid")

#Join player stats with fantasy file to get all player data
player_full = pd.merge(player_stats,fantasy,how="left",on="fullkey")


#Rename columns in full player file and remove uneeded ones
player_full.rename(columns={'matchid_x':'matchid', \
    'disposals_x':'disposals','namekey_x':'namekey'},inplace=True)
player_full.drop(['ha','disposals_y','namekey_y','name','awayline', \
    'awayodds','awayteam','date','homeline','homeodds','hometeam', \
    'round','time','year','matchid_y','namekey_y','fullname'],axis=1,\
    inplace=True)

#Rename columns in match summary file and remove uneeded ones
full_summaries.rename(columns={'round_x':'round', \
    'date_x':'date','time_x':'time'},inplace=True)
full_summaries.drop(['awayteam','hometeam','gameID','date_y', \
    'round_y','date_y','time_y','year'],axis=1,inplace=True)

#Drop any duplicate games
full_summaries.drop_duplicates(subset="matchid",inplace=True)
player_full.drop_duplicates(subset="fullkey",inplace=True)


#Convert blank number fields to zeroes
player_full.replace({r'[^\x00-\x7F]+':0}, regex=True, inplace=True)
full_summaries.replace({r'[^\x00-\x7F]+':0}, regex=True, inplace=True)

#Remove trailing spaces on names
player_full["first_name"] = player_full["first_name"].str.strip()
full_summaries["umpire1"] = full_summaries["umpire1"].str.strip()
full_summaries["umpire2"] = full_summaries["umpire2"].str.strip()
full_summaries["umpire3"] = full_summaries["umpire3"].str.strip()


#Turn stat columns into integers
player_full[['kicks','marks','handballs','disposals','goals', \
             'behinds','hitouts','tackles','rebound50','inside50', \
             'clearances','clangers','frees_for','frees_against', \
             'brownlow', 'contested_poss', 'uncontested_poss', \
             'contested_marks', 'marks_in_50','one_percenters', \
             'bounces', 'goal_assists', 'tog']] = \
player_full[['kicks','marks','handballs','disposals','goals', \
             'behinds','hitouts','tackles','rebound50','inside50', \
             'clearances','clangers','frees_for','frees_against', \
             'brownlow', 'contested_poss', 'uncontested_poss', \
             'contested_marks', 'marks_in_50','one_percenters', \
             'bounces', 'goal_assists', 'tog']].apply(pd.to_numeric)

#Create final scores and make them ints
full_summaries["hscore"] = full_summaries.apply(lambda row: row["hteam_q4"].split(".")[2],axis=1)
full_summaries["ascore"] = full_summaries.apply(lambda row: row["ateam_q4"].split(".")[2],axis=1)
full_summaries ["hscore"] = pd.to_numeric(full_summaries["hscore"])
full_summaries ["ascore"] = pd.to_numeric(full_summaries["ascore"])

#Add season column for player stats
player_full["season"] = player_full.apply(f.fillYear,axis=1)

#Output to CSV
player_full.to_csv("../d.output/players.csv", mode="w", index=False)
full_summaries.to_csv("../d.output/matches.csv", mode="w", index=False)


