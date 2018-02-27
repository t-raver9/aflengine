#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:08:44 2018

@author: chrisstrods
"""
from bs4 import BeautifulSoup
import pandas as pd
import re
import organise as o

#Load an html page and return it as s BS table
def loadPage(u):
    #page = urllib.request.urlopen(u)

    soup = BeautifulSoup(open(u), 'html.parser')

    tables = soup.findChildren('table')

    return tables

#Process and return match summary box
def getSummary(t):
    cells=list()
    for cell in t.findAll("td"):
        cells.append(cell.text)


    matchstring = str(cells[1]).split(" ")


    if(len(cells)==25): #Game finishing in regular time
        umpstring = str(cells[24]).split(",")
    elif(len(cells)==29): #Game finishing in overtime
        umpstring = str(cells[28]).split(",")
    else:
        umpstring = "ERROR"

    #If match is a final, remove 'FINAL' cell so that it aligns with
    #Round numbers
    if(str(matchstring[2]) == "Final"):
        del matchstring[2]


    #Create blank row to be filled
    outrow = [None] * 26
    outrow[0] = matchstring[1] #round


    if(len(matchstring) == 14): #Venue name two words
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","") #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[13] #venue
    elif(len(matchstring) == 13): #Venue name one word
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[12] #venue
    elif(len(matchstring) == 12): #Venue name two words, no crowd
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[11] #venue
    elif(len(matchstring) == 11): #Venue name one word, no crowd
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[10] #venue
    elif(len(matchstring) == 10): #Venue name two words, no venue or timezeone
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = str(matchstring[7]) #date
        outrow[24] = str(matchstring[7].split("-")[2])
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
    elif(len(matchstring) == 9): #Venue name one word, no venue or timezeone
        outrow[1] = matchstring[3] #venue
        outrow[2] = str(matchstring[6]) #date
        outrow[24] = str(matchstring[6].split("-")[2])
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
    else:
        print ("Error with file:" + str(cells[1]) + "   " + str(len(matchstring)))

    outrow[25] = o.getMatchIndex(t)

    #Process teams and quarter by quarter scores for non overtime games
    if(len(cells)==25): #Game finishing in regular time
        outrow[6] = cells[3]    #hteam
        outrow[7] = cells[4]    #hteamQ1
        outrow[8] = cells[5]    #hteamQ2
        outrow[9] = cells[6]    #hteamQ3
        outrow[10] = cells[7]   #hteamQ4
        outrow[11] = cells[8]   #ateam
        outrow[12] = cells[9]   #ateamQ1
        outrow[13] = cells[10]  #ateamQ2
        outrow[14] = cells[11]  #ateamQ3
        outrow[15] = cells[12]  #ateamQ4
    elif(len(cells)==29): #Game finishing in overtime
        outrow[6] = cells[3]    #hteam
        outrow[7] = cells[4]    #hteamQ1
        outrow[8] = cells[5]    #hteamQ2
        outrow[9] = cells[6]    #hteamQ3
        outrow[10] = cells[7]   #hteamQ4
        outrow[11] = cells[9]   #ateam
        outrow[12] = cells[10]   #ateamQ1
        outrow[13] = cells[11]  #ateamQ2
        outrow[14] = cells[12]  #ateamQ3
        outrow[15] = cells[13]  #ateamQ4
        outrow[22] = cells[8]  #hteamET
        outrow[23] = cells[14]  #ateamET


    #Process differently based on howm any umpires in the game
    if(len(umpstring)>2):
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   umpstring[1].split("(")[0]#umpire2
        outrow[18] =   umpstring[2].split("(")[0]
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   re.sub("[^0-9]", "",str(umpstring[1]))
        outrow[21] =   re.sub("[^0-9]", "",str(umpstring[2]))
    elif(len(umpstring)>1):
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   umpstring[1].split("(")[0]#umpire2
        outrow[18] =   ""
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   re.sub("[^0-9]", "",str(umpstring[1]))
        outrow[21] =   ""
    else:
        outrow[16] =   umpstring[0].split("(")[0]
        outrow[17] =   ""
        outrow[18] =   ""
        outrow[19] =   re.sub("[^0-9]", "",str(umpstring[0]))
        outrow[20] =   ""
        outrow[21] =   ""
    return outrow




def getPlayerStats(p,t,ha,s):
    rows=list()
    for row in t.findAll("tr"):
        rows.append(row)

    if(len(rows) <22):
        print("FUCKED UP")
        print(t)
        print(len(rows))
    else:
        rowpoint = 2

        #loop through each player in team
        while(True):
            outrow = [None] * 30
            cells = list()
            for cell in rows[rowpoint].findAll("td"):
                cells.append(cell.text)

            if(cells[0] == "Rushed" or cells[0] == "Totals"):
                break;

            playerID = rows[rowpoint].find("a",href=True)['href'].split("/")[4].split(".")[0]
            team = rows[0].text.split(" Match")[0]





            outrow[0] = playerID
            outrow[1] = o.getMatchIndex(s)
            outrow[2] = o.replaceTeam(team)
            outrow[3] = ha
            outrow[4] = cells[1].split(",")[1]
            outrow[5] = cells[1].split(",")[0]
            outrow[6] = cells[0]
            outrow[7] = cells[2]
            outrow[8] = cells[3]
            outrow[9] = cells[4]
            outrow[10] = cells[5]
            outrow[11] = cells[6]
            outrow[12] = cells[7]
            outrow[13] = cells[8]
            outrow[14] = cells[9]
            outrow[15] = cells[10]
            outrow[16] = cells[11]
            outrow[17] = cells[12]
            outrow[18] = cells[13]
            outrow[19] = cells[14]
            outrow[20] = cells[15]
            outrow[21] = cells[16]
            outrow[22] = cells[17]
            outrow[23] = cells[18]
            outrow[24] = cells[19]
            outrow[25] = cells[20]
            outrow[26] = cells[21]
            outrow[27] = cells[22]
            outrow[28] = cells[23]
            outrow[29] = cells[24]
            p.loc[len(p)] = outrow
            rowpoint += 1
        return p






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




