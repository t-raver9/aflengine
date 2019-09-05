#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 20:29:37 2018

@author: chrisstrods
"""

import pandas as pd
import copy
import random
import laddergen as lg
import numpy as np
from os.path import dirname, abspath

def calcWinProb(df,ratings):
    hteam = df["hteam"]
    ateam = df["ateam"]


    hrating = ratings.loc[hteam]["elo"]
    arating = ratings.loc[ateam]["elo"]


    prob =  1-(1 / (1 + 10 ** ((hrating - arating) / 400)))


    return prob

#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
fixture = pd.read_csv(d+"/bench/extras/fixture2019.csv")
simsummary = pd.read_csv(d+"/bench/extras/simframe.csv")
simsummary = simsummary.set_index("team")
ratings = pd.read_csv(d+"/bench/ratings.csv")
ratings = ratings.set_index("team")


#Get team ratings to current round
fixture.columns = ["round","date","venue","hteam","ateam","result"]
fixture['hteam'] = fixture['hteam'].str.replace('GWS Giants','Greater Western Sydney')
fixture['ateam'] = fixture['ateam'].str.replace('GWS Giants','Greater Western Sydney')
fixture['hteam'] = fixture['hteam'].str.replace('Western Bulldogs','Footscray')
fixture['ateam'] = fixture['ateam'].str.replace('Western Bulldogs','Footscray')
fixture['hteam'] = fixture['hteam'].str.replace('Geelong Cats','Geelong')
fixture['ateam'] = fixture['ateam'].str.replace('Geelong Cats','Geelong')
fixture['hteam'] = fixture['hteam'].str.replace('Adelaide Crows','Adelaide')
fixture['ateam'] = fixture['ateam'].str.replace('Adelaide Crows','Adelaide')
fixture['hteam'] = fixture['hteam'].str.replace('Sydney Swans','Sydney')
fixture['ateam'] = fixture['ateam'].str.replace('Sydney Swans','Sydney')
fixture['hteam'] = fixture['hteam'].str.replace('West Coast Eagles','West Coast')
fixture['ateam'] = fixture['ateam'].str.replace('West Coast Eagles','West Coast')
fixture['hteam'] = fixture['hteam'].str.replace('Gold Coast Suns','Gold Coast')
fixture['ateam'] = fixture['ateam'].str.replace('Gold Coast Suns','Gold Coast')



fixture["hscore"] = fixture.apply(lambda x:int(x['result'].split("-")[0])\
       if type(x['result']) is str else np.nan,axis=1)

fixture["ascore"] = fixture.apply(lambda x:int(x['result'].split("-")[1])\
       if type(x['result']) is str else np.nan,axis=1)

fixture["round"] = fixture.apply(lambda x:str(x['round']),axis=1)

start_ladder =  lg.getLadder(fixture)
remaining_games = fixture[fixture["result"].isnull()]

#Sim remaining games x times
fixture["hwinprob"] = fixture.apply(calcWinProb,axis=1,ratings=ratings)

simresults = []
simladders = []

for i in range (0,1000):
    simmed_games = copy.deepcopy(fixture)
    for index, game in simmed_games.iterrows():
        if(np.isnan(game["hscore"]) == False):
            continue
        r = random.uniform(0, 1)
        if(r<game["hwinprob"]):
            simmed_games.at[index,"hscore"] = 100
            simmed_games.at[index,"ascore"] = 80
        else:
            simmed_games.at[index,"hscore"] = 80
            simmed_games.at[index,"ascore"] = 100

        #print(game)

    simmed_ladder = lg.getLadder(simmed_games)
    simmed_ladder = simmed_ladder.reset_index()

    simresults.append(simmed_games)
    simladders.append(simmed_ladder)
    print("Sim #" + str(i) + " is complete")

i = 1
for sim in simladders:

    #Calc minor premier    
    
    simsummary.loc[sim.iloc[0]["team"]]["p1"] += 1
    simsummary.loc[sim.iloc[1]["team"]]["p2"] += 1
    simsummary.loc[sim.iloc[2]["team"]]["p3"] += 1
    simsummary.loc[sim.iloc[3]["team"]]["p4"] += 1
    simsummary.loc[sim.iloc[4]["team"]]["p5"] += 1
    simsummary.loc[sim.iloc[5]["team"]]["p6"] += 1
    simsummary.loc[sim.iloc[6]["team"]]["p7"] += 1
    simsummary.loc[sim.iloc[7]["team"]]["p8"] += 1
    simsummary.loc[sim.iloc[8]["team"]]["p9"] += 1
    simsummary.loc[sim.iloc[9]["team"]]["p10"] += 1
    simsummary.loc[sim.iloc[10]["team"]]["p11"] += 1
    simsummary.loc[sim.iloc[11]["team"]]["p12"] += 1
    simsummary.loc[sim.iloc[12]["team"]]["p13"] += 1
    simsummary.loc[sim.iloc[13]["team"]]["p14"] += 1
    simsummary.loc[sim.iloc[14]["team"]]["p15"] += 1
    simsummary.loc[sim.iloc[15]["team"]]["p16"] += 1
    simsummary.loc[sim.iloc[16]["team"]]["p17"] += 1
    simsummary.loc[sim.iloc[17]["team"]]["p18"] += 1

    print("Extracted data from sim #" + str(i))
    i += 1


simsummary = simsummary.applymap(lambda x:(x/10000))

simsummary.to_csv(d+"/outputs/finalssim.csv")

#Print outputs

