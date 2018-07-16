#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 19:37:41 2018

@author: chrisstrods
"""

from scipy import stats
import numpy as np
import pandas as pd
from os.path import dirname, abspath
import matplotlib.pyplot as plt

d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/output/matches.csv")
players = pd.read_csv(d + "/output/players.csv")


matches["totalscore"] = matches["hscore"] + matches["ascore"]

matches = matches.loc[matches['season'] >= 2000]

sundays = matches.loc[matches["day"] == "Sun"]


#sundayscores = sundays.groupby(["date"])["totalscore"].sum()

sundayscores = sundays.groupby(["season","round"]).agg({\
                            'totalscore':['sum','mean'],
                            'matchid':['count'],
                            'round':['first'],
                            'season':['first']})

sundayscores.columns = ['scoresum','scoreave','matchcount','tround',\
                      'season',]


seasondays = matches.groupby(["day"]).agg({\
                            'totalscore':['sum','mean'],
                            'matchid':['count'],
                            'round':['first'],
                            'season':['first'],
                            'day':['first']})

seasondays.columns = ['scoresum','scoreave','matchcount','tround',\
                      'season','day']


sundayscores = sundayscores.loc[sundayscores['scoreave'] > 217]

sundayscore3 = sundayscores.loc[sundayscores['matchcount'] >= 3]


roundtoal = 652
roudave = 652 /3