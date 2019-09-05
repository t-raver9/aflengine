#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:49:14 2019

@author: chris
"""

import pandas as pd
from os.path import dirname, abspath

#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
progression = pd.read_csv(d+"/bench/progression.csv")
quarters = pd.read_csv(d+"/bench/quarters.csv")


progressjoin = pd.merge(quarters,progression,how='left',
                        on=['matchid','quarter'])

progressjoin.columns=['matchid','quarter','qminutes','qseconds','team',\
                      'player','type','sminute','ssecond','score']

progressjoin['qlength'] = (progressjoin['qminutes'] * 60) + \
                           progressjoin['qseconds']
                           
progressjoin['scoretime'] = (progressjoin['sminute'] * 60) + \
                           progressjoin['ssecond']
                           
progressjoin.drop(columns=['qminutes','qseconds','sminute','ssecond'],
                  inplace=True)

progressjoin['elapsed'] = progressjoin['scoretime'] / progressjoin['qlength'] * 100


for i, row in progressjoin.iterrows():
    if(i==0):
        progressjoin.at[i,'bouncestart'] = "YES"
    elif(progressjoin.at[i,'quarter'] != progressjoin.at[i-1,'quarter']):
        progressjoin.at[i,'bouncestart'] = "YES"
    elif(progressjoin.at[i-1, 'type'] == "goal"):
        progressjoin.at[i, 'bouncestart'] = "YES"
    else:
        progressjoin.at[i,'bouncestart'] = "NO"

print("DONE")

#progressjoin['bouncestart'] = progressjoin.apply(axis=1,checkbouncestart)