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
test1data = players.loc[players["season"] >=2010]
test1data = test1data.loc[test1data["centre_clearances"].isnull()]


#TEST 2: TO FIND MISSING PLAYER STATS
test2data = players.groupby("matchid").agg('count')["season"].to_frame()
test2data.columns = ['playercount']
test2data = test2data.loc[(test2data['playercount']>44) | \
                          (test2data['playercount']<40)]
