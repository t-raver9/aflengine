#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:42:24 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath


STARTYEAR = 1897 #Year to begin processing data from
STARTELO = 1500 #The default starting ELO rating
MEANELO = 1500
ISRF = 0.1 #Inter season regression factor
K_FACTOR = 40 #K factor for elo - higher = bouncier

class Team:    
    """
    Each team has an instane of this Class, which stores it's ELO
    history, including highs lows and historical values. It also
    tracks what season was the last to be processed for the purpose
    of determining when a new season has started so the ELO score can
    be regressed to the mean
    """
    def __init__(self, name, s_elo):
        self.name = name
        self.elo = s_elo #Starting ELO rating
        self.mean_elo = self.elo
        self.highest_elo = self.elo
        self.lowest_elo = self.elo
        self.last_season = 1896 #Default - does not regress in 1897

def expected(T1, T2, G):
    """
    Calculate expected win likelihood of A in a match against B
    :param T1: Elo rating for Team 1
    :param T2: Elo rating for Team 2
    
    """
    #Calculate home ground weighting    
    #TODO: Make more elaborate
    #function to calculate this more precisely
    if(G=="Home"):
        HGA = 1   
    else:
        HGA = 1
    
    return (1 / (1 + 10 ** ((T2 - T1) / 400))*HGA)

def elo(old, exp, score, k_factor):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    
    return old + k_factor * (score - exp)



def initialiseData():       
    """Intitalise teams data structure and process input file ready for
    ELO calculator"""
    #load matches
    d = dirname(dirname(abspath('__file__')))
    m = pd.read_csv(d + "/elo/elo_matches.csv")
    
    #sort matches by date
    m.sort_values(by=['season', 'date'], inplace=True)

    #Convert dates into a format that can be sorted
    m["date"] = pd.to_datetime(m["date"], \
           dayfirst=True,format="%d/%m/%Y",infer_datetime_format=True)
    m["date"] = m["date"].dt.date
    m = m.loc[m["season"] >= STARTYEAR]

    #Create dictionary of teams with default STARTING ELO
    t = {"Adelaide":Team("Adelaide",STARTELO), \
         "Brisbane Lions":Team("Brisbane Lions",STARTELO), \
         "Brisbane Bears":Team("Brisbane Bears",STARTELO), \
         "Carlton":Team("Carlton",STARTELO), \
         "Collingwood":Team("Collingwood",STARTELO), \
         "Essendon":Team("Essendon",STARTELO),\
         "Fitzroy":Team("Fitzroy",STARTELO), \
         "Footscray":Team("Footscray",STARTELO), \
         "Fremantle":Team("Fremantle",STARTELO), \
         "Geelong":Team("Geelong",STARTELO), \
         "Gold Coast":Team("Gold Coast",STARTELO), \
         "Greater Western Sydney":Team("Greater Western Sydney",STARTELO),\
         "Hawthorn":Team("Hawthorn",STARTELO), \
         "Melbourne":Team("Melbourne",STARTELO), \
         "North Melbourne":Team("North Melbourne",STARTELO),\
         "Port Adelaide":Team("Port Adelaide",STARTELO),\
         "Richmond":Team("Richmond",STARTELO), \
         "St Kilda":Team("St Kilda",STARTELO),\
         "South Melbourne":Team("South Melbourne",STARTELO),\
         "Sydney":Team("Sydney",STARTELO), \
         "West Coast":Team("West Coast",STARTELO),\
         "University":Team("University",STARTELO)}
    
    return t, m


def matchELO(match,teams,teamone,teamtwo,opp_elo):
    """Calculates the new ELO for a single match.
    PARAM:
        match -Row in dataframe with data for a single match
        teams -Dictionary of team ELO data
        teamone -String of team to calculate ELO score for
        teamtwo -String of opponent of team to calculate ELO score for
        opp_elo -The opposition's pre-match ELO"""
    
    #Determine which side was the homse side and apply win factor
    if(teams[teamone].name == match["hteam"]):
        ha = "Home"
        if(match["hscore"] > match["ascore"]):
            factor = 1
        elif(match["hscore"] < match["ascore"]):
            factor = 0
        else:
            factor = 0.5
    else:
        ha = "Away"
        if(match["hscore"] > match["ascore"]):
            factor = 0
        elif(match["hscore"] < match["ascore"]):
            factor = 1
        else:
            factor = 0.5        
    
    
    #If it is the start of new season, wipe of 10% of difference between ELO and 1500
    if(match["season"]==1897):
        pass
    #If it is a new season, update season and adjust ELO
    elif(match["season"]>teams[teamone].last_season):
        teams[teamone].last_season = match["season"]
        if(teams[teamone].elo > MEANELO):
            teams[teamone].elo = teams[teamone].elo - (abs(teams[teamone].elo - MEANELO) * ISRF)
        else:
            teams[teamone].elo = teams[teamone].elo + (abs(teams[teamone].elo - MEANELO) * ISRF)
                    
    new_elo = elo(teams[teamone].elo,             
        expected(teams[teamone].elo,opp_elo,ha),\
        factor, K_FACTOR)   
    
    return new_elo
     
    

def processELO(matches,teams):
    for index, m in matches.iterrows():
        #give each team 0.5 multiple in the match is a draw
        home = m["hteam"]
        away = m["ateam"]
        
        #Make recording of each team's current ELO so they are each
        #Updating against the pre-game value
        h_elo = teams[home].elo
        a_elo = teams[away].elo
        
        #Match ends in a draw
        teams[home].elo = matchELO(m,teams,home,away,a_elo)
        teams[away].elo = matchELO(m,teams,away,home,h_elo)        
    return teams


def postProcess(t):
    r = pd.DataFrame(columns=["team","elo","history"])
    for key, val in list(t.items()):

        r.loc[len(r)] = [key,int(val.elo),""]
        
        r = r[(r.team.str.contains("Fitzroy") == False) & \
        (r.team.str.contains("University") == False) & \
        (r.team.str.contains("Brisbane Bears") == False) & \
        (r.team.str.contains("South Melbourne") == False)]
                
        r.sort_values(by="elo",ascending=False,inplace=True)
    return r
        
      
teams, matches = initialiseData()
teams = processELO(matches,teams)
ranked = postProcess(teams)

