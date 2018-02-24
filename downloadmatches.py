#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 21:24:50 2018

@author: chrisstrods
"""

import json
import os
import urllib


with open('matchlist.json','r') as fin:
    data = json.load(fin)
    
for year, mlist in data.items():
    if(int(year)>2012):
        continue
    print("Downloading " + str(year) + " season")
    if not os.path.exists("matchfiles/" + year):
        os.makedirs("matchfiles/" + year)
    for matchurl in mlist:
        code = str(matchurl).rpartition('/')[2]
        urllib.request.urlretrieve(matchurl, 
                           "matchfiles/" + year + "/" + code)
    print("Successfully downloaded " + str(year) + " season")        
