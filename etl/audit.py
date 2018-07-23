#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:49:12 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath

#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
players = pd.read_csv(d+"/bench/players.csv")
progression = pd.read_csv(d+"/bench/progression.csv")
quarters = pd.read_csv(d+"/bench/quarters.csv")










#### 
#TEST 1: TO FIND INSTANCES WHERE FW AND AT DID NOT JOIN
T1data = players.loc[players["season"] >=2010]
T1data = T1data.loc[T1data["centre_clearances"].isnull()]


#TEST 2: TO FIND MISSING PLAYER STATS
T2data = players.groupby("matchid").agg('count')["season"].to_frame()
T2data.columns = ['playercount']
T2data = T2data.loc[(T2data['playercount']>44) | \
                    (T2data['playercount']<34)]



#TEST 3: CHECK NUMBER OF GAMES PER SEASON
T3data = matches.groupby("season").agg('count')["round"].to_frame()
T3data.columns = ['numgames']


del(d)