#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:19:58 2018

@author: chrisstrods
"""


from scipy import stats
import pandas as pd
from os.path import dirname, abspath

d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/output/matches.csv")
players = pd.read_csv(d + "/output/players.csv")


def getq1(df,t):
    if(t=="a"):
        return int(df["ateam_q1"].split(".")[2])
    else:
        return int(df["hteam_q1"].split(".")[2])
    
def bigquarter(df,t):
    if(t=="a"):
        return max([int(df["ateam_q1"].split(".")[2]),
                    int(df["ateam_q2"].split(".")[2]),
                    int(df["ateam_q3"].split(".")[2]),
                    int(df["ateam_q4"].split(".")[2])])
    else:
        return max([int(df["hteam_q1"].split(".")[2]),
                    int(df["hteam_q2"].split(".")[2]),
                    int(df["hteam_q3"].split(".")[2]),
                    int(df["hteam_q4"].split(".")[2])])


#players = players.loc[players["goals"] >= 3]
#goalkickers = players.groupby("playerid").count()
#sydmatches = matches.loc[(matches["ateam"] == "Sydney") |(matches["hteam"] == "Sydney") ]
#sydmatches["aq1"] = sydmatches.apply(getq1,t="a",axis=1)
#sydmatches["hq1"] = sydmatches.apply(getq1,t="h",axis=1)
#sydmatches = sydmatches.loc[(sydmatches["aq1"] >= 55) | (sydmatches["hq1"] >= 55)]
#sydmatches["big"] = max([sydmatches["hq1"],sydmatches["aq1"]])
#sydmatches["q1margin"] = abs(sydmatches["aq1"]-sydmatches["hq1"])

matches["margin"] = abs(matches["hscore"]-matches["ascore"])
matches["tround"] = matches["round"]
regseason = matches[matches.tround.apply(lambda x: x.isnumeric())]

matchmargins = regseason.groupby(["season","round"]).margin.agg([mean,count])


