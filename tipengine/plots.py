#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:12:09 2020

@author: chris
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from os.path import (
    dirname,
    abspath
)

home_dir = dirname(dirname(abspath(__file__)))
matches = pd.read_csv(home_dir + "/bench/matches.csv")


before2k=matches.loc[matches.gameID > 8936]
after2k=matches.loc[(matches.gameID > 7936) & (matches.gameID <= 8936)]

after2kscores = np.append(after2k.hscore.values,after2k.ascore.values)
before2kscores = np.append(before2k.hscore.values,before2k.ascore.values)



# seaborn histogram
sns.distplot(before2kscores, hist=True, kde=False, 
             bins=max(before2kscores), color = 'blue',
             hist_kws={'edgecolor':'black'})

# seaborn histogram
sns.distplot(after2kscores, hist=True, kde=False, 
             bins=max(after2kscores), color = 'red',
             hist_kws={'edgecolor':'black'})

