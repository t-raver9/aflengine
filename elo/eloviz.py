#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 17:48:08 2018

@author: chrisstrods
"""

import pandas as pd
import plotly 
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


plotly.tools.set_credentials_file(username='chrisstrods', \
                                  api_key='p08RarvxlyCxeqUU0kPS')

elomatches = pd.read_csv("elo_out.csv")

#Select 2018 matches and remove old teams
elo2018 = elomatches.loc[elomatches["season"] == 2018]
elo2018.dropna(axis='columns',inplace=True)


trace0 = go.Scatter(
    x = elo2018["round"],
    y = elo2018["Adelaide"],
    mode = 'lines',
    name = 'lines'
)

trace1 = go.Scatter(
    x = elo2018["round"],
    y = elo2018["Carlton"],
    mode = 'lines',
    name = 'lines'
)

data = [trace0,trace1]

py.iplot(data,filename='line-mode')