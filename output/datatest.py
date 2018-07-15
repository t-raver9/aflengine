#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 21:25:14 2018

@author: chrisstrods
"""

import pandas as pd


matches = pd.read_csv("./matches.csv")
players = pd.read_csv("./players.csv")

missing_fantasy = players.loc[(players["season"] >= 2010) & \
                              (players["Supercoach"].isnull())]