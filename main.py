#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:30:49 2017

@author: chrisstrods
"""

import scrape as s
import pandas as pd

print("Welcome to AFLengine!")

daterange = [1840,1840]
#5088
#4961 - 9414


data = s.loadData(daterange)
playerstats = data[0]
quarterstats = data[1]
matchdetails = data[2]
matchstats = data[3]
brownlow = data[4]


#pd.DataFrame.from_dict(playerstats).to_csv('output/playerstatsEXTRA.csv')
#pd.DataFrame.from_dict(quarterstats).to_csv('output/quarterstatsEXTRA.csv')
#pd.DataFrame.from_dict(matchdetails).to_csv('output/matchdetailsEXTRA.csv')
#pd.DataFrame.from_dict(matchstats).to_csv('output/matchstatsEXTRA.csv')
