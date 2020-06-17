#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 18:21:18 2020

@author: chris
"""

import pandas as pd
import numpy as np
from os.path import dirname, abspath


#load files
d = dirname(dirname(abspath(__file__)))

matches = pd.read_csv(d+"/bench/matches.csv")
matches = matches.loc[matches['homeodds'].notnull()]

matches['faveodds'] = matches.apply(lambda x:min(x['homeodds'],x['awayodds']),axis=1)
matches['winodds'] = matches.apply(lambda x:x['homeodds'] if x['hscore'] > x['ascore'] else x['awayodds'],axis=1)
matches['fpayout'] = matches.apply(lambda x:(x['faveodds']*5)-5 if x['faveodds'] == x['winodds'] else -5,axis=1)

matches['outsideodds'] = matches.apply(lambda x:max(x['homeodds'],x['awayodds']),axis=1)
matches['opayout'] = matches.apply(lambda x:(x['outsideodds']*5)-5 if x['faveodds'] != x['winodds'] else -5,axis=1)
matches['upset'] = matches.apply(lambda x:1 if x['faveodds'] != x['winodds'] else 0,axis=1)


nineteen = matches.loc[matches['season'] == 2019]
eighteen = matches.loc[matches['season'] == 2018]
seventeen = matches.loc[matches['season'] == 2017]

print("2019")
print("Faves: " + str(sum(nineteen['fpayout'])))
print("Outsiders: " + str(sum(nineteen['opayout'])))

print("2018")
print("Faves: " + str(sum(eighteen['fpayout'])))
print("Outsiders: " + str(sum(eighteen['opayout'])))

print("2017")
print("Faves: " + str(sum(seventeen['fpayout'])))
print("Outsiders: " + str(sum(seventeen['opayout'])))


multis = matches.groupby(['season','round']).agg({'faveodds':'prod',\
                                                  'outsideodds':'prod',\
                                                      'upset':'sum'})
    
multis['fpayout'] = multis.apply(lambda x:5*x['faveodds'] if x['upset'] == 0 else -5,axis=1)
multis.reset_index(inplace=True)             
      
multis19 = multis.loc[multis['season']==2019]

