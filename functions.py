#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:08:44 2018

@author: chrisstrods
"""
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re


def loadPage(u):
    page = urllib.request.urlopen(u)

    soup = BeautifulSoup(page, 'html.parser')

    tables = soup.findChildren('table')

    return tables

def getSummary(t):
    cells=list()
    for cell in t.findAll("td"):
        cells.append(cell.text)
    
        
    matchstring = str(cells[1]).split(" ")
    
    if(len(cells)==25):
        umpstring = str(cells[24]).split(",")
    elif(len(cells)==29):
        umpstring = str(cells[28]).split(",")
    else:
        umpstring = "WRONG"
    
    
    if(str(matchstring[2]) == "Final"):
        del matchstring[2]
    
    
        
    outrow = [None] * 22
    outrow[0] = matchstring[1] #round


    if(len(matchstring) == 14): #if venue name is one word
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = matchstring[7] #date
        outrow[3] = matchstring[6].replace(",","") #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[13] #venue
    elif(len(matchstring) == 13):
        outrow[1] = matchstring[3] #venue
        outrow[2] = matchstring[6] #date
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[12] #venue
    elif(len(matchstring) == 12):
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = matchstring[7] #date
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
        outrow[5] = matchstring[11] #venue
    elif(len(matchstring) == 11):
        outrow[1] = matchstring[3] #venue
        outrow[2] = matchstring[6] #date
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        outrow[5] = matchstring[10] #venue
    elif(len(matchstring) == 10):
        outrow[1] = matchstring[3] + " " + matchstring[4] #venue
        outrow[2] = matchstring[7] #date
        outrow[3] = matchstring[6].replace(",","")  #day
        outrow[4] = matchstring[8] #localtime
        #outrow[5] = matchstring[10] #venue 
    elif(len(matchstring) == 9):
        outrow[1] = matchstring[3] #venue
        outrow[2] = matchstring[6] #date
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        #outrow[5] = matchstring[10] #venue
    elif(len(matchstring) == 8):
        outrow[1] = matchstring[3] #venue
        outrow[2] = matchstring[6] #date
        outrow[3] = matchstring[5].replace(",","")  #day
        outrow[4] = matchstring[7] #localtime
        #outrow[5] = matchstring[10] #venue
    else:
        print ("Error with file:" + str(cells[1]) + "   " + str(len(matchstring)))
        
    
    #outrow[1]
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


def initSummaries():
    return pd.DataFrame(columns = ['round','venue','date','day',
                                   'time','crowd','hteam','hteam_q1',
                                   'hteam_q2','hteam_q3','hteam_q4',
                                   'ateam','hteam_q1','hteam_q2',
                                   'hteam_q3','hteam_q4','umpire1',
                                   'umpire2','umpire3','umpire1games',
                                   'umpire2games','umpire3games'])


    