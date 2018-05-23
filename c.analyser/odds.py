#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 19:14:55 2018

@author: chrisstrods
"""

import pandas as pd


def getResultType(df):
    if(df["hscore"]>df["ascore"]):
        if(df["hprob"]>df["aprob"]):
            return "FAVOURITE"
        elif(df["aprob"]>df["hprob"]):
            return "UPSET"
        else:
            return "DEAD HEAT"
    if(df["ascore"]>df["hscore"]):        
        if(df["aprob"]>df["hprob"]):
            return "FAVOURITE"
        elif(df["hprob"]>df["aprob"]):
            return "UPSET"
        else:
            return "DEAD HEAT"
    else:
        return "DRAW"

    
        
       


#load modern data (2010 onwards)
matches = pd.read_csv("../d.output/matches.csv")
matches = matches.loc[matches["season"] >= 2010]

#calculate the vig for each match
matches["overround"]=(1/matches["homeodds"])+(1/matches["awayodds"])
matches["vig"]=100*(matches["overround"]-1)/matches["overround"]
matches["hprob"]=(1/(matches["homeodds"]*matches["overround"])*100) 
matches["aprob"]=(1/(matches["awayodds"]*matches["overround"])*100)
matches["faveprob"]=matches[["hprob","aprob"]].max(axis=1)
matches["upsetprob"]=matches[["hprob","aprob"]].min(axis=1)
matches["results"]=matches.apply(getResultType,axis=1)
