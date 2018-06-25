#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:19:58 2018

@author: chrisstrods
"""


from scipy import stats
import pandas as pd
from os.path import dirname, abspath

d = dirname(dirname(abspath('__file__')))
matches = pd.read_csv(d + "/output/matches.csv")


matches["margin"] = abs(matches["hscore"] - matches["ascore"])

zscores = stats.zscore(matches["margin"])

frimatches = matches.loc[(matches["day"]=="Fri") & (matches["season"] >= 2007)]

means = matches.loc[matches["day"]=="Fri"].groupby(["season"])["margin"].mean()


friteamsh = frimatches.groupby(["hteam"]).agg({'day':['count'],'crowd':['mean']})
friteamsa = frimatches.groupby(["ateam"]).agg({'day':['count'],'crowd':['mean']})
friteams = friteamsh.merge(friteamsa,how="left",left_index=True,right_index=True)

friteams["avecrowd"] = ((friteams['day_x','count']*friteams['crowd_x','mean'])+(friteams['day_y','count']*friteams['crowd_y','mean'])) / ((friteams['day_x','count'] +friteams['day_y','count']))
friteams["totalgames"] = (friteams['day_x','count'] +friteams['day_y','count'])
friteams.columns = ['homegames','avehomecrowd','awaygames','aveawaycrowd','avecrowd','totalgames']