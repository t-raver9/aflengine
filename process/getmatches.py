#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:54:07 2018

@author: chrisstrods
"""

import urllib
from bs4 import BeautifulSoup
import json

base = 'https://afltables.com/afl/seas/'
year = 2017
end = ".html"
matchlist = dict()

while(year>1896):
    url = base + str(year) + end

    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')

    matches = list()

    for a in soup.findAll('a',href=True):
    
        if(a.text=="Match stats"):
            matchstring = "https://afltables.com/afl/" + str(a['href'])[3:]
            matches.append(matchstring)
            matchlist.update({year:matches})
    year -= 1

with open('matchlist.json','w') as fout:
    json.dump(matchlist,fout)
    
    
    



 