#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:42:24 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath
import collections
import copy



STARTYEAR = 1897 #Year to begin processing data from
LASTYEAR = 2018 #Last year data collected
STARTELO = 1500 #The default starting ELO rating
MEANELO = 1500 #Mean ELO to regress to between seasons
ISRF = 0.1 #Inter season regression factor
K_FACTOR = 40 #K factor for elo

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
        self.records = Record()
        self.last_season = 1896 #Default - does not regress in 1897
        
class Record:
    """
    Each team has one of these sitting inside, containing its
    records and details about them
    """
    def __init__(self):
        self.highest_elo = 0
        self.highest_elo_round = ""
        self.highest_elo_season = ""
        self.lowest_elo = 9999
        self.lowest_elo_round = ""
        self.lowest_elo_season = ""


#def calcHGA

def expected(T1, T2, HA, match):
    """
    Calculate expected win likelihood of A in a match against B
    :param T1: Elo rating for Team 1
    :param T2: Elo rating for Team 2
    :param G     
    """
    
    #Calculate home ground advantage factor
    #TODO: base on venue, rather than who is listed as home/away team
    if(HA == "Home"):
        HGA = 50
    else:
        HGA = -50
    
    #Standard formula for calculating ELO probability
    return (1 / (1 + 10 ** ((T2 - T1 + HGA) / 400)))

def elo(old, exp, score, k_factor, match):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    
    #Calculate match ,argin
    margin = abs(match["hscore"] - match["ascore"])
    
    #We want the margin effect to cap out at 80 points
    if(margin > 80):
        margin = 80
    
    #margin_factor should fall with range of 0 and 40
    margin_factor = margin / 2 
    
    
    #Adjusted K is standard K factor plus margin adjustment
    adjusted_k = k_factor + margin_factor
    
    
    return (old + (adjusted_k * (score - exp)))
        



def initialiseData():       
    """Intitalise teams data structure and process input file ready 
    for ELO calculator"""
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
         "Greater Western Sydney":Team("Greater Western Sydney",\
                                       STARTELO),\
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
    
    #Create a season of ELO scores, initialised to 0
    initialiser = collections.OrderedDict({'team':["Adelaide",\
        "Brisbane Bears", "Brisbane Lions","Carlton","Collingwood",\
        "Essendon", "Footscray","Fitzroy","Fremantle","Geelong",\
        "Gold Coast","Greater Western Sydney","Hawthorn","Melbourne",\
        "North Melbourne","Port Adelaide","Richmond","St Kilda",\
        "South Melbourne","Sydney","West Coast","University"
        ],
        'R0':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R1':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R2':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R3':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R4':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R5':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R6':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R7':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R8':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R9':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R10':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R11':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R12':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R13':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R14':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R15':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R16':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R17':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R18':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R19':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R20':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R21':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R22':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R23':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'R24':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'F1':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'F2':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'F3':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
        'F4':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        })

    #Create list of seasons within range
    h = {}
    for i in range(STARTYEAR,LASTYEAR+1):
        h[i] = pd.DataFrame(data=initialiser)
        h[i].set_index('team',inplace=True)
    
    return t, m, h


def matchELO(match,teams,teamone,teamtwo,opp_elo):
    """Calculates the new ELO for a single match.
    PARAM:
        match -Row in dataframe with data for a single match
        teams -Dictionary of team ELO data
        teamone -String of team to calculate ELO score for
        teamtwo -String of opponent of team to calculate ELO score for
        opp_elo -The opposition's pre-match ELO"""
    
    #Determine which side was the home side and apply win factor
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
    
    
    #If it is the start of new season, wipe off 10% of 
    #difference between ELO and 1500
    if(match["season"]==1897):
        pass
    #If it is a new season, update season and adjust ELO
    elif(match["season"]>teams[teamone].last_season):
        teams[teamone].last_season = match["season"]
        if(teams[teamone].elo > MEANELO):
            teams[teamone].elo = teams[teamone].elo - \
                (abs(teams[teamone].elo - MEANELO) * ISRF)
        else:
            teams[teamone].elo = teams[teamone].elo + \
                (abs(teams[teamone].elo - MEANELO) * ISRF)
                    

    #Calculate new ELO based on match result
    new_elo = elo(teams[teamone].elo,             
        expected(teams[teamone].elo,opp_elo,ha,match),\
        factor, K_FACTOR,match)   
    
    return new_elo

#Change round names for finals     
def updateRound(r):
    if(r == "Qualifying" or r== "Elimination"):
        out = "F1"
    elif(r == "Semi"):
        out = "F2"
    elif(r == "Preliminary"):
        out = "F3"
    elif(r == "Grand"):
        out = "F4"
    else:
        out = "R" + str(r)
        
    return out

def processELO(matches,teams, history):
    for index, m in matches.iterrows():
        #give each team 0.5 multiple in the match is a draw
        home = m["hteam"]
        away = m["ateam"]
        season = m["season"]
        the_round = m["round"]
        
        the_round = updateRound(the_round)
        
        #Make recording of each team's current ELO so they are each
        #Updating against the pre-game value
        h_elo = teams[home].elo
        a_elo = teams[away].elo
        
        if(the_round == "R1"):
            history[season].loc[home]["R0"] = teams[home].elo + \
                ((MEANELO - teams[home].elo)*ISRF)
            history[season].loc[away]["R0"] = teams[away].elo + \
                ((MEANELO - teams[away].elo)*ISRF)
        
        #Update teams structure
        teams[home].elo = matchELO(m,teams,home,away,a_elo)
        teams[away].elo = matchELO(m,teams,away,home,h_elo)   
        
        
        #Update historical score matrix
        history[season].loc[home][the_round] = teams[home].elo
        history[season].loc[away][the_round] = teams[away].elo        
        
        
        
    return teams, history


def fillBlankRounds(df,n):
    if(df[[n]] != 0):
        return df[[n]]
    else:
        if(n==0):
            return df[[n+1]]
        else:
            for x in range (1,27):
                if(df[[n-x]] != 0):
                    return df[[n-x]]
                
            
        
  

def postProcess(t,h,syear,lyear):
    r = pd.DataFrame(columns=["team","elo","history"])
    for key, val in list(t.items()):

        r.loc[len(r)] = [key,int(val.elo),""]
        
                
        r.sort_values(by="elo",ascending=False,inplace=True)
        
        r = r.loc[(r['team'] != 'Fitzroy') & \
                  (r['team'] != 'South Melbourne') & \
                  (r['team'] != 'Brisbane Bears') & \
                  (r['team'] != 'University')]
          
        
        
        
        for i in range(syear,lyear+1):
            #Remove any team which was not active in that season
            #Note becuase of byes, check to make sure team didn't play
            #In consecutive weeks
            h[i] = h[i][(h[i].R2 != 0) | (h[i].R3 != 0)]
            
            #Remove any rounds which were not played that season
            h[i] = h[i][h[i].columns[(h[i]!=0).any(axis=0)]]
            
            #Fill zero rounds from when a team didn't play with the 
            #previous rounds
            length = len(h[i].index)
            
            for n in range(0,28):
                try:
                    inspect_round = h[i].iloc[:,n]
                    if(n==0):
                        prior_round = h[i].iloc[:,n+1]    
                    else:
                        prior_round = h[i].iloc[:,n-1]
                    
                    for x in range(0,length):
                        if(inspect_round.iloc[x] != 0):
                            continue
                        else:
                            inspect_round[x] = prior_round[x]
                except IndexError:
                    continue
            
            
        
        
    return r, h


def getRecords(history,teams):
    

    
    for t_key,team in teams.items():
        for s_key,season in history.items():
            t_season = season[season.index == t_key]
            for x in range(0,len(t_season.columns)):
                try:
                    curr_round = int(t_season.iloc[:,x][0])
                       
                    cols = list(t_season.columns.values)
                    if(curr_round > team.records.highest_elo):
                        team.records.highest_elo = curr_round
                        team.records.highest_elo_round = cols[x]
                        team.records.highest_elo_season = s_key
                        
                    if(curr_round < team.records.lowest_elo):
                        team.records.lowest_elo = curr_round
                        team.records.lowest_elo_round = cols[x]
                        team.records.lowest_elo_season = s_key
                        
                except IndexError:
                    continue
                    
    
    
    
    return teams
    

def getRecordSummary(teams):
    
    record_table = pd.DataFrame(columns=['elo_high','elo_high_round',\
        'elo_high_season','elo_low','elo_low_round','elo_low_season'])
    
    for key, value in teams.items():
        record = value.records
        record_table.loc[value.name] = [record.highest_elo,\
            record.highest_elo_round,record.highest_elo_season,\
            record.lowest_elo,record.lowest_elo_round,\
            record.lowest_elo_season]
        
    return record_table
        

#    
def prepareOutput(h):
    
    output = pd.DataFrame()

    for key, value in h.items():
        new_df = value.transpose()
        new_df["season"] = str(key)
        new_df["round"] = new_df.index
        new_df["new_index"] = new_df["season"] + new_df["round"]
        new_df.set_index("new_index",inplace=True)        
        output = output.append(new_df)
    return output

    
  
teams, matches, history = initialiseData()
modern_teams = copy.deepcopy(teams)
teams, history = processELO(matches, teams, history)
current, history = postProcess(teams,history,1897,2018)
teams = getRecords(history,teams)
test = prepareOutput(history)

#modern_teams = copy.deepcopy(teams)
modern_details = dict((k,history[k])for k in range(2010,2019))
modern_teams = getRecords(modern_details,modern_teams)
modern_summary = getRecordSummary(modern_teams)



record_summary = getRecordSummary(teams)


print(current["elo"].mean())

test.to_csv("elo_out.csv",mode="w")



