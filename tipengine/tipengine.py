#!/usr/bin/env pyton3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:34:20 2020

@author: chris
"""

import pandas as pd

fixture2020 =  pd.read_csv('fixture2020.csv')
tips2020 =  pd.read_csv('tips2020.csv')
tally2020 =  pd.read_csv('tally2020.csv',index_col='tipper')

rnd = "1"

tippers = tally2020.index.values


fixture2020['key'] = fixture2020['round'] + fixture2020['hometeam'] + fixture2020['awayteam']
tips2020['key'] = tips2020['round'] + tips2020['hometeam'] + tips2020['awayteam'] 
combined = fixture2020.merge(tips2020,on='key',how='inner')


for tipper in tippers:
    score = 0
    games = combined.loc[combined['round_x'] == rnd]
    for index, row in games.iterrows():
        if(row[tipper] == row['winner']):
           score += 1
    tally2020.at[tipper,"r"+rnd] = score
    

tally2020.to_csv('tally2020.csv')
           
  
