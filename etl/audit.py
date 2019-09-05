#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:49:12 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath

# load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d + "/bench/matches.csv")
players = pd.read_csv(d + "/bench/players.csv")
progression = pd.read_csv(d + "/bench/progression.csv")
quarters = pd.read_csv(d + "/bench/quarters.csv")

pt = players.head(100)

####
# TEST 1: TO FIND INSTANCES WHERE FW AND AT DID NOT JOIN
# Pass criteria: Zero rows in T1Data
T1data = players.loc[players["season"] >= 2010]
T1data = T1data.loc[T1data["centre_clearances"].isnull()]

# TEST 2: TO FIND MISSING OR SURPLUS PLAYER STATS
# Pass criteria: One row in T2data (1996 blackout game)
T2data = players.groupby("matchid").agg('count')["season"].to_frame()
T2data.columns = ['playercount']
T2data = T2data.loc[(T2data['playercount'] > 44) | \
                    (T2data['playercount'] < 34)]

# TEST 3: CHECK NUMBER OF GAMES PER SEASON
# Check AFLtables for total number of games
T3data = matches.groupby("season").agg('count')["round"].to_frame()
T3data.columns = ['numgames']

# TEST 4: CHECK HOME TEAMS CORRECTLY IDENTIFIED
T4data = matches.groupby(["hteam", "venue"]).agg('count')["round"].to_frame()
T4data.columns = ['numgames']

# TEST 5: CHECK NUMBER OF INDIVIDUAL PLAYERS
# Confirm with AFLtables number of players
T5data = len(players.groupby("playerid").agg('count')["kicks"].to_frame().index)

# TEST 6: Check missing 2018 games
T6data = matches.loc[matches['season'] == 2018]
T6count = T6data.groupby("round").agg('count')

del (d)
