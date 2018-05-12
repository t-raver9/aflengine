#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:42:24 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath

def getWinner(df):
    if(df["hscore"] > df["ascore"]):
        return df["hteam"]
    elif(df["hscore"] < df["ascore"]):
        return df["ateam"]
    else:
        return "Draw"
    
def getLoser(df):
    if(df["hscore"] > df["ascore"]):
        return df["ateam"]
    elif(df["hscore"] < df["ascore"]):
        return df["hteam"]
    else:
        return "Draw"
    
def getWinscore(df):
    if(df["hscore"] > df["ascore"]):
        return df["hscore"]
    elif(df["hscore"] < df["ascore"]):
        return df["ascore"]
    else:
        return df["hscore"]

def getLosescore(df):
    if(df["hscore"] < df["ascore"]):
        return df["hscore"]
    elif(df["hscore"] > df["ascore"]):
        return df["ascore"]
    else:
        return df["hscore"]

def expected(A, B):
    """
    Calculate expected win likelihood of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, k_factor):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    return old + k_factor * (score - exp)


class Team:    
    def __init__(self, name, s_elo):
        self.name = name
        self.elo = 1500
        self.mean_elo = self.elo
        self.highest_elo = self.elo
        self.lowest_elo = self.elo
        self.last_season = 1896
        
#load matches
d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/elo/elo_matches.csv")

#sort matches by date
matches.sort_values(by=['season', 'date'], inplace=True)

#create columns for winning team and losing team
matches["Wteam"] = matches.apply(getWinner,axis=1)
matches["Lteam"] = matches.apply(getLoser,axis=1)
matches["Wscore"] = matches.apply(getWinscore,axis=1)
matches["Lscore"] = matches.apply(getLosescore,axis=1)

#ELO contstants
mean_elo = 1500
elo_width = 500
k_factor = 30

m_trim = matches.head(100)


#Convert dates into datetime object
matches["date"] = pd.to_datetime(matches["date"], \
       dayfirst=True,format="%d/%m/%Y",infer_datetime_format=True)
matches["date"] = matches["date"].dt.date
matches = matches.loc[matches["season"] > 1897]

teams = {"Adelaide":Team("Adelaide",1500), \
         "Brisbane Lions":Team("Brisbane Lions",1500), \
         "Brisbane Bears":Team("Brisbane Bears",1500), \
         "Carlton":Team("Carlton",1500), \
         "Collingwood":Team("Collingwood",1500), \
         "Essendon":Team("Essendon",1500),\
         "Fitzroy":Team("Fitzroy",1500), \
         "Footscray":Team("Footscray",1500), \
         "Fremantle":Team("Fremantle",1500), \
         "Geelong":Team("Geelong",1500), \
         "Gold Coast":Team("Gold Coast",1500), \
         "Greater Western Sydney":Team("Greater Western Sydney",1500),\
         "Hawthorn":Team("Hawthorn",1500), \
         "Melbourne":Team("Melbourne",1500), \
         "North Melbourne":Team("North Melbourne",1500),\
         "Port Adelaide":Team("Port Adelaide",1500),\
         "Richmond":Team("Richmond",1500), \
         "St Kilda":Team("St Kilda",1500),\
         "South Melbourne":Team("South Melbourne",1500),\
         "Sydney":Team("Sydney",1500), \
         "West Coast":Team("West Coast",1500),\
         "University":Team("University",1500)}






for index, m in matches.iterrows():
    #give each team 0.5 multiple in the match is a draw
    if(m["Wteam"] == "Draw"):
        home = m["hteam"]
        away = m["ateam"]
        if(m["season"]==1896):
            pass
        elif(m["season"]>teams[home].last_season):
            teams[home].last_season = m["season"]
            if(teams[home].elo > 1500):
                teams[home].elo = int(teams[home].elo - (abs(teams[home].elo - 1500) * .1))
            else:
                teams[home].elo = int(teams[home].elo + (abs(teams[home].elo - 1500) * .1))
        if(m["season"]==1896):
            pass
        elif(m["season"]>teams[away].last_season):
            teams[away].last_season = m["season"]
            if(teams[away].elo > 1500):
                teams[away].elo = int(teams[away].elo - (abs(teams[away].elo - 1500) * .1)) 
            else:
                teams[away].elo = int(teams[away].elo + (abs(teams[away].elo - 1500) * .1)) 
        
        teams[home].elo = int(elo(teams[home].elo,             
            expected(teams[home].elo,teams[away].elo),\
            0.5, k_factor))     
        teams[away].elo = int(elo(teams[away].elo,
            expected(teams[away].elo,teams[home].elo),\
            0.5, k_factor))
    else:
        winner = m["Wteam"]
        loser = m["Lteam"]
        
        #If it is the start of new season, wipe of 20% of difference between ELO and 1500
        if(m["season"]==1896):
            pass
        elif(m["season"]>teams[winner].last_season):
            teams[winner].last_season = m["season"]
            if(teams[winner].elo > 1500):
                teams[winner].elo = int(teams[winner].elo - (abs(teams[winner].elo - 1500) * .1))
            else:
                teams[winner].elo = int(teams[winner].elo + (abs(teams[winner].elo - 1500) * .1))
        if(m["season"]==1896):
            pass        
        elif(m["season"]>teams[loser].last_season):
            teams[winner].last_season = m["season"]
            if(teams[loser].elo > 1500):
                teams[loser].elo = int(teams[loser].elo - (abs(teams[loser].elo - 1500) * .1))
            else:
                teams[loser].elo = int(teams[loser].elo + (abs(teams[loser].elo - 1500) * .1))


        new_elo = elo(teams[winner].elo,
            expected(teams[winner].elo,teams[loser].elo),1, \
            k_factor)        
        teams[winner].elo = int(new_elo)
        
        new_elo = elo(teams[loser].elo,
            expected(teams[loser].elo,teams[winner].elo),0, \
            k_factor)                
        teams[loser].elo = int(new_elo)
            
ranked = pd.DataFrame(columns=["team","elo","history"])

for key, val in list(teams.items()):
    if(val.elo==1500):
        del teams[key]
    else:
        ranked.loc[len(ranked)] = [key,val.elo,""]
        
ranked = ranked[(ranked.team.str.contains("Fitzroy") == False) & \
            (ranked.team.str.contains("University") == False) & \
            (ranked.team.str.contains("Brisbane Bears") == False) & \
            (ranked.team.str.contains("South Melbourne") == False)]
                
ranked.sort_values(by="elo",ascending=False,inplace=True)
        
        

print(ranked["elo"].mean())

print(expected(1611,1350))
print("Expected odds:" + str(100/(expected(1621,1545)*100)))
print("Expected odds:" + str(100/(expected(1545,1621)*100)))
