#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 20:04:26 2018

@author: chrisstrods
"""

import pandas as pd
from os.path import dirname, abspath

#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")

matches["margin"] = abs(matches["hscore"] - matches["ascore"])
hundredpoints = matches.loc[(matches["hscore"]>=100) | (matches["ascore"]>=100)]
hundredpoints["hscoreflag"] = hundredpoints.apply(lambda x:x["hscore"] > 100)

matches = matches[pd.to_numeric(matches['round'], errors='coerce').notnull()]
closegames = matches.loc[matches["margin"] >6]


roundmargins = matches.groupby(["season","round"]).agg({'margin':['mean','count']})
roundmargins.columns=["avemargin","games"]
roundmargins = roundmargins.loc[roundmargins["games"] >= 8]


closegamecount = closegames.groupby(["season","round"]).count()


