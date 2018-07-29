#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:24:48 2018

@author: chrisstrods
"""


import pandas as pd
from os.path import dirname, abspath
import re

#load files
d = dirname(dirname(dirname(abspath(__file__))))

progression = pd.read_csv(d+"/bench/progression.csv")
quarters = pd.read_csv(d+"/bench/quarters.csv")

matchprog = progression.loc[progression["matchid"] == "2017PFADEGEE"]
matchq = quarters.loc[quarters["matchid"] == "2017PFADEGEE"]

matchprog["hscore"] = int(re.split('.-',matchprog["score"]))[2]


matchmins = matchq.iloc[0]["minutes"] + \
            matchq.iloc[1]["minutes"] + \
            matchq.iloc[2]["minutes"] + \
            matchq.iloc[3]["minutes"] + \
            int(60/(matchq.iloc[0]["seconds"] + \
                    matchq.iloc[1]["seconds"] + \
                    matchq.iloc[2]["seconds"] + \
                    matchq.iloc[3]["seconds"]))


matchsecs = (matchq.iloc[0]["seconds"] + \
             matchq.iloc[1]["seconds"] + \
             matchq.iloc[2]["seconds"] + \
             matchq.iloc[3]["seconds"])%60

matchlength = matchmins + (matchsecs / 60)


                    
                    