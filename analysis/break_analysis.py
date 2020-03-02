#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 21:32:16 2020

@author: chris
"""

import pandas as pd

def whoWins(df):
    if(df["hscore"] > df["ascore"]):
        return "Home"
    elif(df["hscore"] < df["ascore"]):
        return "Away"
    else:
        return "Draw"

def getMonth(df):
    return df["date"].split("-")[1]

def advantageWho(df):
    if(df["home_day_diff"] > 0):
        return "Home"
    elif(df["home_day_diff"] < 0):        
        return "Away"
    else:
        return "Nobody"

def didBreakHelp(df):
    if(df["advantage"] == "Nobody"):
        return "N/A"
    elif(df["advantage"] == df["who_wins"]):        
        return "Helped"
    else:
        return "Did not help"



data = pd.read_csv("../bench/matches_plus.csv", low_memory=False)

data = data.loc[data["season"] >= 2015]

data["home_day_diff"] = data["h_break"] - data["a_break"]
data['home_day_diff'][data['home_day_diff'] >= 1] = 1
data['home_day_diff'][data['home_day_diff'] <= -1] = -1
data['advantage'] = data.apply(advantageWho,axis=1)
data['home_day_diff'] = abs(data['home_day_diff'])


data["who_wins"] = data.apply(whoWins,axis=1)
data["month"] = data.apply(getMonth,axis=1)

data["longer_break_win"] = data.apply(didBreakHelp,axis=1)

#Do it broken down by months
break_table = data.groupby("home_day_diff")['longer_break_win'].apply(lambda x: x[x.str.contains('Helped')].count()).to_frame()
break_table['did_not_help'] = data.groupby("home_day_diff")['longer_break_win'].apply(lambda x: x[x.str.contains('Did not help')].count())
break_table.columns = ['helped','did_not_help']
break_table['help_win_percentage'] = break_table.apply(lambda x: x['helped']/(x['helped']+x['did_not_help']),axis=1)
break_table['nohelp_win_percentage'] = break_table.apply(lambda x: x['did_not_help']/(x['helped']+x['did_not_help']),axis=1)



#Do it broken down by months
break_table_month = data.groupby(["home_day_diff","month"])['longer_break_win'].apply(lambda x: x[x.str.contains('Helped')].count()).to_frame()
break_table_month['did_not_help'] = data.groupby(["home_day_diff","month"])['longer_break_win'].apply(lambda x: x[x.str.contains('Did not help')].count())
break_table_month.columns = ['helped','did_not_help']
break_table_month['help_win_percentage'] = break_table_month.apply(lambda x: x['helped']/(x['helped']+x['did_not_help']),axis=1)
break_table_month['nohelp_win_percentage'] = break_table_month.apply(lambda x: x['did_not_help']/(x['helped']+x['did_not_help']),axis=1)
        

break_table_month.to_csv("break_table_month.csv")

