#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:31:50 2018

@author: chrisstrods
"""

import pandas as pd
from pandasql import sqldf
from os.path import dirname, abspath


#load matches
d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/output/matches.csv")

#Convert dates into datetime object
matches["date"] = pd.to_datetime(matches["date"], \
       dayfirst=True,format="%d/%m/%Y",infer_datetime_format=True)
matches["date"] = matches["date"].dt.date

#Exlude matches before 1990
#matches = matches.loc[matches["date"] > datetime.date(1990,1,1)]


pdsql = lambda q: sqldf(q, globals())
q  = """
    SELECT 
        date,
        season,
        round,
        hteam,
        ateam,
        hscore,
        ascore,
        venue,
        date,
        day,
        time,
        homeline,
        awayline,
        homeodds,
        awayodds
        
    FROM 
        matches;
        """
trimmed_matches = pdsql(q)


trimmed_matches.to_csv("elo_matches.csv", mode="w", index=False)