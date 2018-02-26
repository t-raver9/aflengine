#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:49:21 2018

@author: chrisstrods
"""
import pandas as pd


#Create unique ID for each game, based on year, round, and teamcode
def createIndex(df):
    df['date'].replace("/","-")
    year = df['season']
    tround = getRoundCode(df['round'])
    hcode = getTeamCode(df['hteam'])
    acode = getTeamCode(df['ateam'])
    gindex = str(year) + str(tround) + hcode + acode
    return gindex    
        
        #Assign game index to each game




def replaceTeam(team):
    if(team=="Western Bulldogs"):
        return "Footscray"
    elif(team=="Kangaroos"):
        return "North Melbourne"
    else:
        return team

#Generate a three character 'teamcode' for each team    
def getTeamCode(team):
    return {
           'Adelaide' : 'ADE',
           'Brisbane Bears' : 'BBL',
           'Brisbane Lions' : 'BRS',
           'Carlton' : 'CAR',
           'Collingwood' : 'COL',
           'Essendon' : 'ESS',
           'Fitzroy' : 'FIT',
           'Footscray' : 'FOT',
           'Fremantle' : 'FRE',
           'Geelong' : 'GEE',
           'Gold Coast' : 'GCS',
           'Greater Western Sydney' : 'GWS',
           'Hawthorn' : 'HAW',
           'Melbourne' : 'MEL',
           'North Melbourne' : 'NOR',
           'Port Adelaide' : 'POR',
           'Richmond' : 'RCH',
           'South Melbourne' : 'SMS',
           'St Kilda' : 'STK',
           'Sydney' : 'SYD',
           'University' : 'UNI',
           'West Coast' : 'WEG'
           }[team]

#Turns each round into two characters    
def getRoundCode(round):
    return {
           '1' : '01',
           '2' : '02',
           '3' : '03',
           '4' : '04',
           '5' : '05',
           '6' : '06',
           '7' : '07',
           '8' : '08',
           '9' : '09',
           '10' : '10',
           '11' : '11',
           '12' : '12',
           '13' : '13',
           '14' : '14',
           '15' : '15',
           '16' : '16',
           '17' : '17',
           '18' : '18',
           '19' : '19',
           '20' : '20',
           '21' : '21',
           '22' : '22',
           '23' : '23',
           '24' : '24',
           'Elimination' : 'EF',
           'Qualifying' : 'QF',
           'Semi' : 'SF',
           'Preliminary' : 'PF',
           'Grand' : 'GF'
           }[round]    
           
def getMatchIndex(m):
    cells=list()
    for cell in m.findAll("td"):
        cells.append(cell.text)
    
        
    matchstring = str(cells[1]).split(" ")
    
    
    #If match is a final, remove 'FINAL' cell so that it aligns with
    #Round numbers
    if(str(matchstring[2]) == "Final"):
        del matchstring[2]
    
    
    #Create blank row to be filled    

    theround = matchstring[1] #round


    if(len(matchstring) == 14): #Venue name two words
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 13): #Venue name one word
        year = str(matchstring[6].split("-")[2])
    elif(len(matchstring) == 12): #Venue name two words, no crowd
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 11): #Venue name one word, no crowd
        year = str(matchstring[6].split("-")[2])
    elif(len(matchstring) == 10): #Venue name two words, no venue or timezeone
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 9): #Venue name one word, no venue or timezeone
        year = str(matchstring[6].split("-")[2])
    else:
        print ("Error with file:" + str(cells[1]) + "   " + str(len(matchstring)))
        
    
    #Process teams and quarter by quarter scores for non overtime games
    if(len(cells)==25): #Game finishing in regular time
        hteam = cells[3]    #hteam
        ateam = cells[8]   #ateam
    elif(len(cells)==29): #Game finishing in overtime
        hteam = cells[3]    #hteam
        ateam = cells[9]   #ateam

    hcode = getTeamCode(replaceTeam(hteam))
    acode = getTeamCode(replaceTeam(ateam))
    rcode = getRoundCode(theround)
    
    return (str(year) + str(rcode) + hcode + acode)

        
if __name__ == '__main__':    

    summaries_f = open("../outputs/match_summaries.csv")
    summaries = pd.DataFrame.from_csv(summaries_f)

    summaries['game_index'] = ""

    #Replace 'Western Bulldogs' with 'Footscray' and 'Kangaroos' 
    #with 'North Melbourne
    summaries['ateam'].replace(to_replace="Western Bulldogs",
             value="Footscray",inplace=True)
    summaries['hteam'].replace(to_replace="Western Bulldogs",
             value="Footscray",inplace=True)
    summaries['ateam'].replace(to_replace="Kangaroos",
             value="Footscray",inplace=True)
    summaries['hteam'].replace(to_replace="Kangaroos",
             value="North Melbourne",inplace=True)
    
    #Apply game index
    summaries['game_index'] = summaries.apply(createIndex, axis=1)
    
    summaries.to_csv("../outputs/match_summaries_indexes.csv", mode="w")
    

    
