# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 18:16:31 2020

@author: chris
"""


import pandas as pd
from os.path import dirname, abspath

try:
    import shared_functions as f
except ModuleNotFoundError:
    from etl import shared_functions as f


def main():
    #load files
    d = dirname(dirname(abspath(__file__)))

    summaries = pd.read_csv(d+"/staging/match_summaries.csv")
    player_stats = pd.read_csv(d+"/staging/player_stats.csv",low_memory=False)
    odds = pd.read_csv(d+"/staging/odds_data.csv")
    fantasy = pd.read_csv(d+"/staging/fantasy_scores.csv")
    adv_stats = pd.read_csv(d+"/staging/adv_stats.csv")
    quarters = pd.read_csv(d+"/staging/q_lengths.csv")
    progression = pd.read_csv(d+"/staging/scoring_progression.csv")
    
    #Drop any records which have been scraped twice
    summaries.drop_duplicates(inplace=True)
    player_stats.drop_duplicates(inplace=True)
    odds.drop_duplicates(inplace=True)
    fantasy.drop_duplicates(inplace=True)
    adv_stats.drop_duplicates(inplace=True)
    quarters.drop_duplicates(inplace=True)
    progression.drop_duplicates(inplace=True)
    
    summaries.to_csv(d+"/staging/match_summaries.csv", index=False)
    player_stats.to_csv(d+"/staging/player_stats.csv", index=False)
    odds.to_csv(d+"/staging/odds_data.csv", index=False)
    fantasy.to_csv(d+"/staging/fantasy_scores.csv", index=False)
    adv_stats.to_csv(d+"/staging/adv_stats.csv", index=False)
    quarters.to_csv(d+"/staging/q_lengths.csv", index=False)
    progression.to_csv(d+"/staging/scoring_progression.csv", index=False)    

    
#main()