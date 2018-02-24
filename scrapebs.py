#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:31:18 2018

@author: chrisstrods
"""


import functions as f
import os

folder ='/Users/chrisstrods/AnacondaProjects/aflengine/matchfiles/'
year = 2017


match_summaries = f.initSummaries()

while(year>1896):
    print("Processing year: " + str(year))
    files = os.listdir(folder + str(year))


    for file in files:
        rawmatch = f.loadPage("file://" + folder + str(year) + "/" + file)
        match_summaries.loc[len(match_summaries)] = f.getSummary(rawmatch[0])
    
    year -= 1



match_summaries.to_csv("./outputs/match_summaries2.csv", mode="w")

#rawmatch = f.loadPage(folder)





#match_summary= match[0]
#home_stats= match[2]
#away_stats= match[4]
#home_details= match[5]
#away_details= match[6]
#score_progression= match[7]






