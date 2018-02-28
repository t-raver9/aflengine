#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:19:21 2018

@author: chrisstrods
"""
import numpy as np
import pandas as pd

summaries = pd.read_csv("../outputs/match_summaries_index.csv")
player_stats = pd.read_csv("../outputs/player_stats.csv_index",dtype=[])