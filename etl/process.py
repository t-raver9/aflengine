#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 20:30:04 2018

@author: chrisstrods
"""

import pandas as pd
import shared_functions as f
from os.path import dirname, abspath



#load files
d = dirname(dirname(abspath(__file__)))


summaries = pd.read_csv(d+"/staging/match_summaries.csv")
player_stats = pd.read_csv(d+"/staging/player_stats.csv")
odds = pd.read_csv(d+"/staging/odds_data.csv")
fantasy = pd.read_csv(d+"/staging/fantasy_scores.csv")
adv_stats = pd.read_csv(d+"/staging/adv_stats.csv")
quarters = pd.read_csv(d+"/staging/q_lengths.csv")
progression = pd.read_csv(d+"/staging/scoring_progression.csv")


#Drop any records which have been scraped twice
summaries.drop_duplicates(subset="matchid",inplace=True)
player_stats.drop_duplicates(inplace=True)
odds.drop_duplicates(subset="gameID",inplace=True)
fantasy.drop_duplicates(inplace=True)
adv_stats.drop_duplicates(inplace=True)
quarters.drop_duplicates(inplace=True)
progression.drop_duplicates(inplace=True)


#######
#
# PROCESS PLAYER STATS AND MATCH SUMMARIES
#
#######


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

#Generate merge columns to get join key for advanced stats file
adv_stats["fullname"] = fantasy.apply(f.nameClean,axis=1)
adv_stats["namekey"] = fantasy.apply(f.getNameKeyFW,axis=1)
adv_stats["fullkey"] = fantasy.apply(f.getFullKey,axis=1)


#Generate merge columns to get join key for player stats file
player_stats["namekey"] = player_stats.apply(f.getNameKeyAT,axis=1)
player_stats["fullkey"] = player_stats.apply(f.getFullKey,axis=1)

#Join match summaries with odds file to get all match data
full_summaries = pd.merge(summaries,odds,how="left",on="matchid")

#Join player stats with fantasy file and advanced stats file to get all player data
player_temp = pd.merge(player_stats,fantasy,how="left",on="fullkey")
player_full = pd.merge(player_temp,adv_stats,how="left",on="fullkey")

pf = player_full.head(100)


#Rename columns in full player file and remove uneeded ones
player_full.rename(columns={'matchid_x':'matchid', \
                            'kicks_x':'kicks',\
                            'homeAway_x':'homeAway',\
                            'name_x':'name',\
                            'fullname_x':'fullnane'},inplace=True)
player_full.drop(['ha','kicks_y','namekey_y','name','homeAway_y',\
                  'awayline','awayodds','awayteam','date',\
                  'homeline','homeodds','hometeam', 'round',\
                  'time','year','matchid_y','namekey_y','name_y',\
                  'fullname','fullname_y','namekey_x'],axis=1,\
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
             'bounces', 'goal_assists', 'tog','BO',\
             'centre_clearances','CM','CP','disposal_efficiency',\
             'effective_disposals','GA','intercepts','metres_gained',\
             'MI5','P1','stoppage_clearances','score_involvements',\
             'tackles_inside_50','turnovers','UP']] = \
player_full[['kicks','marks','handballs','disposals','goals', \
             'behinds','hitouts','tackles','rebound50','inside50', \
             'clearances','clangers','frees_for','frees_against', \
             'brownlow', 'contested_poss', 'uncontested_poss', \
             'contested_marks', 'marks_in_50','one_percenters', \
             'bounces', 'goal_assists', 'tog','BO','CCL','CM',\
             'CP','DE','ED','GA','ITC','MG','MI5','P1','SCL','SI',\
             'T5','TO','UP']].apply(pd.to_numeric)
player_full.drop(['BO','CM','CP','GA','MI5','P1','UP','CCL','DE',\
                  'ED','ITC','MG','SCL','SI','T5','T0'],axis=1,inplace=True)

#Create final scores and make them ints
full_summaries["hscore"] = full_summaries.apply(lambda row: row["hteam_q4"].split(".")[2],axis=1)
full_summaries["ascore"] = full_summaries.apply(lambda row: row["ateam_q4"].split(".")[2],axis=1)
full_summaries ["hscore"] = pd.to_numeric(full_summaries["hscore"])
full_summaries ["ascore"] = pd.to_numeric(full_summaries["ascore"])

#Add season column for player stats
player_full["season"] = player_full.apply(f.fillYear,axis=1)




#######
#
# PROCESS SCORING PROGRESSION AND QUARTER LENGTHS
#
#######
quarters["minutes"] = quarters.apply(lambda row: int(row["minutes"].replace("m","")),axis=1)
quarters["seconds"] = quarters.apply(lambda row: int(row["seconds"].replace("s","")),axis=1)

progression["minutes"] = progression.apply(lambda row: int(row["minutes"]),axis=1)
progression["seconds"] = progression.apply(lambda row: int(row["seconds"]),axis=1)
progression["quarter"] = progression.apply(lambda row: int(row["quarter"]),axis=1)



#Output to CSV
player_full.to_csv(d+"/bench/players.csv", mode="w", index=False)
full_summaries.to_csv(d+"/bench/matches.csv", mode="w", index=False)
progression.to_csv(d+"/bench/progression.csv", mode="w", index=False)
quarters.to_csv(d+"/bench/quarters.csv", mode="w", index=False)
