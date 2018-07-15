#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:08:44 2018

@author: chrisstrods
"""
from bs4 import BeautifulSoup
import pandas as pd
import numpy


#Load an html page and return it as s BS table
def loadPage(u):
    #page = urllib.request.urlopen(u)

    soup = BeautifulSoup(open(u), 'html.parser')

    tables = soup.findChildren('table')

    return tables


#Output row to the table
def initSummaries():
    return pd.DataFrame(columns = ['round','venue','date','day',
                                   'time','crowd','hteam','hteam_q1',
                                   'hteam_q2','hteam_q3','hteam_q4',
                                   'ateam','ateam_q1','ateam_q2',
                                   'ateam_q3','ateam_q4','umpire1',
                                   'umpire2','umpire3','umpire1games',
                                   'umpire2games','umpire3games',
                                   'hteam_et','ateam_et','season','matchid'])

def initPlayerStats():
    return pd.DataFrame(columns=['playerid','matchid','team','ha','first_name','last_name',
                                   'number','kicks','marks','handballs',
                                   'disposals','goals','behinds',
                                   'hitouts','tackles','rebound50',
                                   'inside50','clearances','clangers',
                                   'frees_for','frees_against',
                                   'brownlow','contested_poss',
                                   'uncontested_poss','contested_marks',
                                   'marks_in_50','one_percenters',
                                   'bounces','goal_assists','tog'])


#Create unique ID for each game, based on year, round, and teamcode
def createIndex(df):
    df['date'].replace("/","-")
    year = df['season']
    tround = getRoundCode(df['round'])
    hcode = getTeamCode(df['hteam'])
    acode = getTeamCode(df['ateam'])
    codes = [hcode,acode]
    codes.sort()
    
    
    gindex = str(year) + str(tround) + codes[0] + codes[1]
    return gindex

        #Assign game index to each game


def replaceTeam(team):
    if(team=="Western Bulldogs"):
        return "Footscray"
    elif(team=="Kangaroos"):
        return "North Melbourne"
    else:
        return team
    
    
def getMatchID(df):
    hcode = getTeamCode(df['hometeam'])
    acode = getTeamCode(df['awayteam'])
    codes = [hcode,acode]
    codes.sort()
    
    return (str(df["year"]) + str(getRoundCode(df["round"])) + \
            codes[0] + codes[1])
    
def nameFormat(df,col):
    if(df[col] == "Western Bulldogs"):
        return "Footscray"
    elif(df[col] == "Kangaroos"):
        return "North Melbourne"
    elif(df[col] == "Brisbane"):
        return "Brisbane Lions"
    elif(df[col] == "GWS"):
        return "Greater Western Sydney"
    else:
        return df[col]
        

def getPlayerMatchID(df):
    playerID = str(df["name"]).replace(" ","_")
    
    
    if(numpy.isnan(df["addcode"])):
        return str(playerID) + str(df["matchid"])
    else:
        return str(playerID) + str(df["matchid"]) + str(+ df["addcode"])
    


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

    r = str(round)

    try:
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
                'Grand' : 'GF',
                'Final' : 'TF'

                }[r]

    except KeyError:
        print("Error for round: " + str(round))

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
    
    codes = [hcode,acode]
    codes.sort()

    rcode = getRoundCode(theround)

    return (str(year) + str(rcode) + codes[0] + codes[1])

def cleanNumber(df):
    if(len(str(df["number"])) > 2):
        return df["number"][:2]
    else:
        return df["number"]

#checks if a player was subbed on or off an creates a column for it
def checkSub(df):
    if(len(str(df["number"])) > 2):
        if("↓" in str(df["number"])):
            return "off"
        elif("↑" in str(df["number"])):
            return "on"
        else:
            return ""
    else:
        return ""
    
def changeDate(date):
    dstring = date.split(' ')
    newdate = str(dstring[1].strip('stndrh') + " " + dstring[2] + " " + dstring[3])
    return newdate

def convertStats(file,content):
    f = pd.read_csv(file, index_col = 0)
    m=[]
    if(content == "Match"):
         for index, row in f.iterrows():
             m.append({'gameID':row["gameID"],'ha':"Home", 'team':row["hometeam"], 'kicks':row["homekicks"],
                    'hb':row["homehb"], 'disp':row["homedisp"], 'marks':row["homemarks"], 
                    'tackles':row["hometackles"], 'hitouts':row["homehitout"], 'ff':row["homeff"],
                    'fa':row["homeff"], 'goals':row["homeg"], 'behinds':row["homebk"], 'score':(row["homeg"] * 6) + row["homebk"], 
                    'margin':(row["homeg"] * 6) + row["homebk"] - ((row["awayg"] * 6) + row["awaybk"]),'rushed':row["homerush"], 'i50':row["homei50"]})
    
             m.append({'gameID':row["gameID"], 'ha':"Away",'team':row["awayteam"], 'kicks':row["awaykicks"],
                    'hb':row["awayhb"], 'disp':row["awaydisp"], 'marks':row["awaymarks"], 
                    'tackles':row["awaytackles"], 'hitouts':row["awayhitout"], 'ff':row["awayff"],
                    'fa':row["awayff"], 'goals':row["awayg"], 'behinds':row["awaybk"], 'score':(row["awayg"] * 6) + row["awaybk"], 
                    'margin':(row["awayg"] * 6) + row["awaybk"] - ((row["homeg"] * 6) + row["homebk"]), 'rushed':row["awayrush"], 'i50':row["awayi50"]})
    return pd.DataFrame.from_dict(m)


def getYear(df):
#<<<<<<< HEAD
    #date = df["date"].split("/")
    #return "20" + date[2]
    return pd.to_datetime(df["date"]).year
    #return df["date"].year
#=======
#    date = df["date"].split("/")
#    return "20" + date[2]
#>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85

def getNameKeyFW(df):
    namesplit = df["fullname"].split(" ")
    one = namesplit[0][0]
    
    if("." in namesplit[1]):
        two = namesplit[2]
    else:
        two = namesplit[1]
        
    try:
        d = int(df["kicks"])
    except ValueError:
        d = 0
    
    three = str(d)
    return str(one + two + three).lower()

def getNameKeyAT(df):
    one = df["first_name"][1]
    two = df["last_name"].split(" ")[0]
    
    try:
        d = int(df["kicks"])
    except ValueError:
        d = 0
    
    three = str(d)
    return str(one + two + three).lower()

def getFullKey(df):
    return df["matchid"] + df["namekey"]

def fillYear(df):
    yearstring = df["matchid"][:4]
    return int(yearstring)

def nameClean(df):
    return {
            'Gary Jnr Ablett': 'Gary Ablett',
            'Darcy BJones' : 'Darcy ByrneJones',
            'Josh DCardillo' : 'Josh Deluca',
            'Trent DLane' : 'Trent DennisLane',
            'Cameron EYolmen' : 'Cam EllisYolmen',
            'Michael S Gardiner' : 'Michael Gardiner',
            'George HSmith' : 'George HorlinSmith',
            'Will HElliott' : 'Will HoskinElliott',
            'Jarrod KThomson' : 'Jarrod KaylerThomson',
            'Josh P Kennedy' : 'Josh Kennedy',
            'Jay KHarris' : 'Jay Kennedy',
            'Nathan LMurray' : 'Nathan LovettMurray',
            'Anthony MTipungwuti' : 'Anthony McDonaldTipungwuti',
            'Alex NBullen' : 'Alex NealBullen',
            'Sam PSeton' : 'Sam PetrevskiSeton',
            'Sam PPepper' : 'Sam PowellPepper',
            'Lewis RThomson' : 'Lewis RobertsThomson',
            'Ed VWillis' : 'Ed VickersWillis',
            'Luke DUniacke' : 'Luke DaviesUniacke'

            }.get(df["name"],df["name"])
    
            #return NAMESWAP.get(df.loc[])
            #str(df["fullname"])

