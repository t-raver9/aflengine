# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:37:30 2020

@author: chris
"""


import pandas as pd
from pandasql import sqldf
from os.path import dirname, abspath


#load matches
d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/bench/matches.csv")

progress = pd.read_csv(d + "/bench/progression.csv")


progress['season'] = progress['matchid'].apply(lambda x:int(x[0:4]))

progress = progress.loc[progress['season']>=2017]

progress['timeon'] = progress.apply(lambda x:1 if x['minutes'] >=20 else 0,axis=1)
progress['plus25'] = progress.apply(lambda x:1 if x['minutes'] >=25 else 0,axis=1)




progress.to_csv('timeon.csv')