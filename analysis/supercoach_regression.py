#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 16:01:24 2018

@author: chrisstrods
"""

from scipy import stats
import numpy as np
import pandas as pd
from os.path import dirname, abspath
import matplotlib.pyplot as plt

d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/output/matches.csv")
players = pd.read_csv(d + "/output/players.csv")


def getMCGCount(df):
    if((df["venue"] == "M.C.G.") or (df["venue"] == "Docklands")):
        return 1
    else:
        return 0


#This is for supercoach plots
'''matches = matches.loc[matches["season"] >= 2010]
players = players.loc[players["season"] >= 2010]

players_sc = players.groupby(["matchid"])["Supercoach"].sum()

matches = matches.merge(players_sc.to_frame(),right_index=True,left_on="matchid")
matches = matches.loc[(matches["Supercoach"] > 2510) & (matches["Supercoach"] < 5000)]
print(np.mean(matches["Supercoach"]))
print(np.std(matches["Supercoach"]))
plt.ylim(3000,3500)
plt.hist(matches["Supercoach"],normed=True,bins=20)
plt.boxplot(matches["Supercoach"])


matches["sc_total"]  = players_sc#= players.merge(players_sc,how="Left",right_index=True,left_on="matchid")




#matches["margin"] = abs(matches["hscore"] - matches["ascore"])
#matches_sc = matches.groupby(["matchid"])["margin"].mean()


#matches["margin"] = abs(matches["hscore"] - matches["ascore"])'''


matches["melbcount"] = matches.apply(getMCGCount,axis=1)

satmatches = matches.loc[matches["day"] == "Sat"]
satmatches = satmatches.loc[satmatches["crowd"] > 0]

attendance = satmatches.groupby(["season","round"]).agg({\
                            'crowd':['sum','mean'],
                            'matchid':['count'],
                            'round':['first'],
                            'season':['first'],
                            'melbcount':['sum']})

attendance.columns = ['crowdsum','crowdave','matchcount','tround',\
                      'season','melbgame']
attendance = attendance.loc[attendance["matchcount"] >= 3]
attendance = attendance.loc[attendance["melbgame"] > 1]
attendance = attendance[attendance.tround.apply(lambda x: x.isnumeric())]
attendance["tround"] = attendance["tround"].apply(pd.to_numeric)

crowd = 10181 + 26693 + 21430
crowdave = crowd / 3

lowerattendance = attendance.loc[attendance["crowdave"] < crowdave]







hawmatches = matches.loc[matches["hteam"] == "Hawthorn"]
hawmatches = hawmatches.loc[matches["venue"] == "M.C.G."]