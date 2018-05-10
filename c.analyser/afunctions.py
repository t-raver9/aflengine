#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:47:24 2018

@author: chrisstrods
"""

def getPoints(df):
    return int(df["hteam_q4"].split(".")[2]) + \
            int(df["ateam_q4"].split(".")[2])
            
def getAccuracy(df):
    goals = int(df["hteam_q4"].split(".")[0]) + \
        int(df["ateam_q4"].split(".")[0])
    
    behinds = int(df["hteam_q4"].split(".")[1]) + \
        int(df["ateam_q4"].split(".")[1])
    return (goals / (goals + behinds) * 100)


def getUmpGames(df):
    games = df["umpire1games"] + df["umpire2games"] + df["umpire3games"]
    return games

